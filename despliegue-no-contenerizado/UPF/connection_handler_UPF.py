import socket
from utils_UPF import receive_data, send_bytes

def handle_client(conn, addr, addresses):
    """Maneja la conexión con un cliente."""
    "addr es la ip del cliente que se conecta"
    "addresses es el diccionario con las distintas ips que manda el NRF"
    print(f"New client connected from {addr[0]}:{addr[1]}")

    try:
        message = receive_data(conn)
        print(f"Received message from {addr} (hex): {message.hex()}")
        print(f"Received message from {addr} (decimal): {list(message)}")

        # Añadir un byte extra al final del mensaje como identificador del UPF
        upf_identifier = b'\x01'  # Puedes cambiar este valor según sea necesario
        message += upf_identifier

        # Conectar al SMF
        conn_SMF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_SMF.connect(tuple(addresses["SMF"]))

        print(f"Redirecting message to SMF")

        if send_bytes(conn_SMF, message):
            response = receive_data(conn_SMF)
            if response:
                print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                conn_SMF.close()
     
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

