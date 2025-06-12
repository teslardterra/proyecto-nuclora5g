import socket
import threading
from connection_handler_NRF import handle_client


def get_local_ip():
    """Obtiene la IP local asignada al contenedor dentro de la red Docker."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Configuración del servidor
IP = get_local_ip()
PORT = 5050
ADDR = (IP, PORT)
BACKLOG = 1000

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""
    print("[NRF][STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[NRF][LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[NRF][ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
