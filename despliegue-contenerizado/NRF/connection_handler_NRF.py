import json
from utils_NRF import receive_data, return_addresses

def handle_client(conn, addr):
    """Maneja la conexión con un cliente."""
    print(f"New client connected from {addr[0]}:{addr[1]}")

    try:
        message = receive_data(conn)

        if message:
            print("Addresses request received")
            response = return_addresses()
            response_json = json.dumps(response)
            conn.send(response_json.encode('utf-8'))
            print(f"Sent response to {addr}: {response_json}")

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")