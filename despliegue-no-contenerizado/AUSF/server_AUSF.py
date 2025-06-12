import socket
import threading
from connection_handler_AUSF import handle_client
from utils_AUSF import ask_nrf_for_addresses

# Configuración del servidor
ADDR = ("127.0.0.1", 5054)
BACKLOG = 1000

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""

    addresses = ask_nrf_for_addresses()
    print(f"[AUSF] Addresses received: {addresses}")
    print("[AUSF] [STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[AUSF] [LISTENING] Server is listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, addresses))
        thread.start()
        print(f"[AUSF] [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
