import socket
import json
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import time
import random


ADDR_NRF = ("127.0.0.1", 5050)

def receive_data(conn, buffer_size=1024):
    """
    Recibe datos del servidor.
    :param conn: El objeto de conexión del servidor.
    :param buffer_size: Tamaño del búfer para recibir datos.
    :return: Los datos recibidos como bytes, o None si no se recibieron datos.
    """
    try:
        data = conn.recv(buffer_size)
        return data if data else None
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

def send_bytes(conn, data):
    """
    Envía un array de bytes al servidor.
    :param conn: El objeto de conexión del servidor.
    :param data: Los datos a enviar (como bytes o bytearray).
    :return: True si los datos se enviaron correctamente, False en caso contrario.
    """
    try:
        conn.send(data)  # Envía los datos en bruto (bytes)
        print(f"Bytes enviados: {data}")
        return True
    except Exception as e:
        print(f"Error sending bytes: {e}")
        return False

def send_string(conn, message):
    """
    Envía una cadena de texto al servidor.
    :param conn: El objeto de conexión del servidor.
    :param message: La cadena de texto a enviar.
    :return: True si el mensaje se envió correctamente, False en caso contrario.
    """
    try:
        conn.send(message.encode('utf-8'))  # Codifica el mensaje en UTF-8
        print(f"Mensaje enviado: {message}")
        return True
    except Exception as e:
        print(f"Error sending string: {e}")
        return False

def ask_nrf_for_addresses():
    """
    Pide al NRF las direcciones de los demás componentes.
    :return: Un diccionario con las direcciones de los componentes.
    """
    message = "Requesting addresses"

    try:
        # Crear una conexión al NRF
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(ADDR_NRF)

        # Enviar el mensaje al NRF
        send_string(conn, message)

        # Recibir la respuesta del NRF
        response_bytes = receive_data(conn)
        if response_bytes:
            response_json = response_bytes.decode('utf-8')
            addresses = json.loads(response_json)
            return addresses
        else:
            print("No response received from NRF")
            return None

    except Exception as e:
        print(f"Error asking NRF for addresses: {e}")
        return None

    finally:
        conn.close()

def identify_connection(message):
    """
    Identifica la conexión en función del último byte del mensaje.
    :param message: El mensaje recibido.
    :return: "UPF" si el último byte del mensaje es 0x01, "UNKNOWN" en caso contrario.
    """
    if message[-1] == 0x01:
        return "UPF"
    if message[-1] == 0x02:
        return "SMF"
    if message[-1] == 0x03:
        return "AMF"
    if message[-1] == 0x04:
        return "AUSF"
    return "UNKNOWN"

def identify_payload_type(message):
    """
    Identifica el tipo de payload en función del primer byte del mensaje.
    :param message: El mensaje recibido.
    :return: "Authentication" si el primer byte del mensaje es 0x00, "Data" en caso contrario.
    """
    if message[0] == 0x00:
        return "Authentication"
    return "Data"


def sessiondb_open_new_session(DeviceID, key, session_nonce, derivation_nonce, session_duration):
    tiempo_espera = random.uniform(0.1, 0.7)

    # Esperar el tiempo generado
    time.sleep(tiempo_espera)
    conn_db = sqlite3.connect(r'C:\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()
    SessionDerivatedKey = key
    SessionNonce = session_nonce
    SessionDuration = session_duration
    SessionCounter = 0
    DerivationNonce = derivation_nonce

    cursor.execute('''CREATE TABLE IF NOT EXISTS SessionsLoRa
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       DeviceID BLOB NOT NULL,          
                       SessionNonce BLOB NOT NULL, 
                       DerivationNonce BLOB NOT NULL,          
                       SessionDuration INTEGER,         
                       SessionCounter INTEGER,         
                       SessionDerivatedKey BLOB NOT NULL)''')

    cursor.execute("SELECT SessionDerivatedKey, SessionNonce, SessionDuration, SessionCounter, DerivationNonce FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    if result:
        # Si existe, actualiza los campos
        cursor.execute("""
            UPDATE SessionsLoRa
            SET SessionDerivatedKey=?, SessionNonce=?, SessionDuration=?, SessionCounter=?, DerivationNonce=?
            WHERE DeviceID=?
        """, (SessionDerivatedKey, SessionNonce, SessionDuration, SessionCounter, DerivationNonce, DeviceID))
    else:
        # Si no existe, inserta una nueva fila
        cursor.execute("""
            INSERT INTO SessionsLoRa (DeviceID, SessionDerivatedKey, SessionNonce, SessionDuration, SessionCounter, DerivationNonce)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (DeviceID, SessionDerivatedKey, SessionNonce, SessionDuration, SessionCounter, DerivationNonce))

    conn_db.commit()
    conn_db.close()
    return result


def session_check_DeviceID(DeviceID):

    conn_db = sqlite3.connect(r'C:\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()

    cursor.execute("SELECT * FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    print(f"result: {result}")  # Para ver el resultado de la consulta
    conn_db.close()
    return result

def session_retrieve_data(DeviceID):

    conn_db = sqlite3.connect(r'C\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()
    
    cursor.execute("SELECT SessionNonce, DerivationNonce, SessionDerivatedKey FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    print(f"result: {result}")  # Para ver el resultado de la consulta
    conn_db.close()
    return result

def chacha20_decrypt(encrypted_data: bytes, key: str, nonce_number: int) -> bytes:
    """
    Desencripta datos en bytes usando ChaCha20.
    
    :param encrypted_data: Bytes encriptados.
    :param key: Clave en formato hexadecimal.
    :param nonce_number: Nonce como número entero.
    :return: Bytes desencriptados.
    """
    key = bytes.fromhex(key)[:32]
    nonce = nonce_number.to_bytes(16, 'big')

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(encrypted_data)
    
    return decrypted_data

def session_nonce_addone(DeviceID):

    conn_db = sqlite3.connect(r'C:\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()

    # Recuperar el valor de SessionNonce
    cursor.execute("SELECT SessionNonce FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    if result:
        session_nonce = result[0]
        # Convertir de BLOB a int
        session_nonce_int = int.from_bytes(session_nonce, byteorder='big')
        # Aumentar en 1 su valor
        if session_nonce_int == 255:
            session_nonce_int = 0
        else:
            session_nonce_int += 1
        # Convertir de nuevo a bytes
        new_session_nonce = session_nonce_int.to_bytes((session_nonce_int.bit_length() + 7) // 8, byteorder='big')
        # Actualizar el nuevo valor en la base de datos
        cursor.execute("UPDATE SessionsLoRa SET SessionNonce=? WHERE DeviceID=?", (new_session_nonce, DeviceID))
        conn_db.commit()

    conn_db.close()


def update_and_check_session_counter(DeviceID):

    conn_db = sqlite3.connect(r'C:\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()

    # Recuperar el valor de SessionCounter y SessionDuration
    cursor.execute("SELECT SessionCounter, SessionDuration FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    if result:
        session_counter, session_duration = result
        # Incrementar en 1 el valor de SessionCounter
        session_counter += 1

        if session_counter >= session_duration:
            # Si SessionCounter coincide con SessionDuration, eliminar la fila
            cursor.execute("DELETE FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
            print(f"Session duration reached for DeviceID {DeviceID}. Session removed.")
        else:
            # Actualizar el nuevo valor de SessionCounter en la base de datos
            cursor.execute("UPDATE SessionsLoRa SET SessionCounter=? WHERE DeviceID=?", (session_counter, DeviceID))
        
        conn_db.commit()

    conn_db.close()



def update_and_check_session_counter_lost_case(DeviceID, decrypted_SessionNonce):

    conn_db = sqlite3.connect(r'C:\SessionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()

    # Recuperar la fila que tenga el DeviceID proporcionado
    cursor.execute("SELECT SessionCounter, SessionNonce, SessionDuration FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    if result:
    
        session_counter, session_nonce, session_duration = result
        # Convertir SessionNonce y decrypted_SessionNonce a ints
        session_nonce_int = int.from_bytes(session_nonce, byteorder='big')
        decrypted_session_nonce_int = int.from_bytes(decrypted_SessionNonce, byteorder='big')

        # Diferencia entre nonces
        diff =  (decrypted_session_nonce_int - session_nonce_int) % 256
        session_counter += diff
        session_counter += 1

        if session_counter < session_duration:
            print(f"In range, message accepted, session updated")
            cursor.execute("""
            UPDATE SessionsLoRa
            SET SessionNonce=?, SessionCounter=?
            WHERE DeviceID=?
            """, (decrypted_SessionNonce, session_counter, DeviceID))
            conn_db.commit()
            return True
        elif session_counter == session_duration:
            print(f"In range, message accepted, session removed")
            cursor.execute("DELETE FROM SessionsLoRa WHERE DeviceID=?", (DeviceID,))
            conn_db.commit()
            conn_db.close()
            return True
        else:
            print(f"Out of range, message discarded")
            return False
    conn_db.close()

