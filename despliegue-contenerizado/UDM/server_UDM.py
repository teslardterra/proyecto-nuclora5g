import socket
import threading
from connection_handler_UDM import handle_client
from utils_UDM import ask_nrf_for_addresses

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
ADDR = (get_local_ip(), 5055)
BACKLOG = 1000

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""

    addresses = ask_nrf_for_addresses()
    print(f"[UDM] Addresses received: {addresses}")
    print("[UDM] [STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[UDM] [LISTENING] Server is listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, addresses))
        thread.start()
        print(f"[UDM] [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
