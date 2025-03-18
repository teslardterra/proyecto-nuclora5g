import socket
import json
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import datetime
import time
import random

ADDR_NRF = ("192.168.70.130", 5050)

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
    ADDR_NRF = ("127.0.0.1", 5050)
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

def FLA_check_DeviceID(message):
   
    conn_db = sqlite3.connect(r'./SubscribersLoRa.db', timeout=10)
    cursor = conn_db.cursor()

    print(f"message: {message}")  # Para ver el valor que se está pasando
    
    cursor.execute("SELECT * FROM SuscribersLoRa WHERE DeviceID=?", (message,))
    result = cursor.fetchone()

    print(f"result: {result}")  # Para ver el resultado de la consulta
    conn_db.close()
    return result

def SLA_retrieve_data(message):

    conn_db = sqlite3.connect(r'./SubscribersLoRa.db', timeout=10)
    cursor = conn_db.cursor()
    DeviceID = message[:3]
    
    cursor.execute("SELECT PSK, PSCC, SessionDuration FROM SuscribersLoRa WHERE DeviceID=?", (DeviceID,))
    result = cursor.fetchone()

    print(f"result: {result}")  # Para ver el resultado de la consulta
    conn_db.close()
    return result

def store_transmission(DeviceID, data_type, data):

    conn_db = sqlite3.connect(r'./TransmissionsLoRa.db', timeout=10)
    cursor = conn_db.cursor()
    
    # Crear una nueva fila en la base de datos
    cursor.execute("INSERT INTO TransmissionsLoRa (DeviceID, Received_at, Received_data, Data_type) VALUES (?, ?, ?, ?)",
              (DeviceID, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data, data_type))
    
    # Guardar los cambios
    conn_db.commit()
    
    conn_db.close()
    return True

def derive_key(cadena1, cadena2, nonce, longitud_clave=32):
    # Convierte las tuplas de enteros a bytes y luego combina
    combinacion = bytes(cadena1) + bytes(cadena2) + nonce
    
    # Utiliza PBKDF2 para derivar una clave de longitud especificada
    clave = PBKDF2(combinacion, nonce, dkLen=longitud_clave)
    
    return clave
