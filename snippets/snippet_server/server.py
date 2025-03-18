import socket
import threading
from connection_handler import handle_client

# Configuración del servidor
IP = "127.0.0.1"
PORT = 5050
ADDR = (IP, PORT)
BACKLOG = 1000

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""
    print("[STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
