import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
import hashlib


ADDR_NRF = (socket.gethostbyname("contenedor-nrf"), 5050)

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

def obtain_3_md5_bytes(datos: bytes) -> bytes:
    """Calcula el hash MD5 de los datos proporcionados y retorna los 3 primeros bytes."""
    md5_hash = hashlib.md5()
    md5_hash.update(datos)
    return md5_hash.digest()[:3]
