import socket
import json

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