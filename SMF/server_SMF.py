import socket
import threading
from connection_handler_SMF import handle_client
from utils_SMF import ask_nrf_for_addresses

# Configuración del servidor
ADDR = ("192.168.70.136", 5052)
BACKLOG = 1000

# Lock para procesar clientes uno a la vez
lock = threading.Lock()

def client_wrapper(conn, addr, addresses):
    """Envuelve el manejo del cliente con un Lock para procesar uno a la vez."""
    with lock:
        handle_client(conn, addr, addresses)
    conn.close()

def start_server():
    """Inicia el servidor y maneja las conexiones entrantes."""

    addresses = ask_nrf_for_addresses()
    print(f"[SMF] Addresses received: {addresses}")
    print("[SMF] [STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(BACKLOG)
    print(f"[SMF] [LISTENING] Server is listening on {ADDR[0]}:{ADDR[1]}")

    while True:
        conn, addr = server.accept()
        print(f"[SMF] [NEW CONNECTION] {addr} connected.")
        thread = threading.Thread(target=client_wrapper, args=(conn, addr, addresses))
        thread.start()
        thread.join()  # Espera a que el cliente actual termine antes de aceptar otro
        print(f"[SMF] [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
