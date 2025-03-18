import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def chacha20_encrypt(data: bytes, key: str, nonce_number: int) -> bytes:
    """
    Encripta datos en bytes usando ChaCha20.
    
    :param data: Bytes a encriptar.
    :param key: Clave en formato hexadecimal.
    :param nonce_number: Nonce como número entero.
    :return: Bytes encriptados.
    """
    key = bytes.fromhex(key)[:32]  # Asegurar 32 bytes de clave
    nonce = nonce_number.to_bytes(16, 'big')  # Convertir número a 16 bytes

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_data = encryptor.update(data)
    
    return encrypted_data

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

def derivar_clave(cadena1, cadena2, nonce, longitud_clave=32):
    # Convierte las tuplas de enteros a bytes y luego combina
    combinacion = bytes(cadena1) + bytes(cadena2) + nonce
    
    # Utiliza PBKDF2 para derivar una clave de longitud especificada
    clave = PBKDF2(combinacion, nonce, dkLen=longitud_clave)
    
    return clave


# Configuración del servidor
SERVER_IP = "127.0.0.1"  # Dirección IP del servidor
SERVER_PORT = 5051        # Puerto del servidor
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

def receive_data(conn, buffer_size=1024):
    """
    Recibe datos del servidor.
    :param conn: El objeto de conexión del servidor.
    :param buffer_size: Tamaño del búfer para recibir datos (por defecto 1024 bytes).
    :return: Los datos recibidos como bytes, o None si no se recibieron datos.
    """
    try:
        data = conn.recv(buffer_size)
        if data:
            return data  # Devuelve los datos en bruto (bytes)
        return None
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

def send_message():
    """Envía un array de bytes y una cadena de texto al servidor."""
    try:
        device_id = bytes([0x01, 0x02, 0x03])  # DeviceID de 3 bytes
        psk = bytes([0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13])  # PSK de 16 bytes
        pscc = bytes([0xAA, 0xBB, 0xCC])  
        derivation_nonce =  bytes([0x11])
        session_nonce = bytes([0x00])
        
        key = derivar_clave(device_id, psk, derivation_nonce).hex()
        
        # Crea un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conecta al servidor
        client_socket.connect(SERVER_ADDR)
        print(f"Conectado al servidor en {SERVER_IP}:{SERVER_PORT}")

        # Envía un array de 51 bytes (por ejemplo, lleno de ceros salvo los primeros 3 bytes)
        byte_array = bytearray(51)  # Array de 51 bytes inicializados a 0
        for i in range(51):
            byte_array[i] = i
        
        byte_array[0] = 0x00  # MENSAJE AUTENTICACIÓN
        byte_array[1:4] = device_id
        byte_array[4] = derivation_nonce[0]
        byte_array[5] = session_nonce[0]
        byte_array[6:9] = list(pscc)
       
        print("Array de bytes sin encriptar:", byte_array.hex())
        # Seleccionar los bytes que deseas encriptar (por ejemplo, del índice 0 al 3)
        start_index = 5
        end_index = 8  # Ahora end_index es inclusivo
        bytes_a_encriptar = byte_array[start_index:end_index + 1]  # Usamos end_index + 1

        # Encriptar los bytes seleccionados
        bytes_encriptados = chacha20_encrypt(bytes_a_encriptar, key, int.from_bytes(derivation_nonce, 'big'))
        print(f"key {key}")
        
        print("llegado")
        # Reemplazar los bytes originales en el array con los bytes encriptados
        byte_array[start_index:end_index + 1] = bytes_encriptados  # Usamos end_index + 1
        print("Array de bytes modificado (encriptado):", byte_array.hex())
        if send_bytes(client_socket, byte_array):
            # Recibe la respuesta del servidor
            response = receive_data(client_socket)
            if response:
                print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cierra la conexión
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    send_message()

