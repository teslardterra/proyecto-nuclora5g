import socket
import threading
from connection_handler_UPF import handle_client
from utils_UPF import ask_nrf_for_addresses

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
port = 5051
ADDR = (IP, port)
BACKLOG = 1000

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""

    addresses = ask_nrf_for_addresses()
    print(f"[UPF] Addresses received: {addresses}")
    print("[UPF] [STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[UPF][LISTENING] Server is listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, addresses))
        thread.start()
        print(f"[UPF] [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
