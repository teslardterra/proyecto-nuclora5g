from utils import receive_data

def handle_client(conn, addr):
    """Maneja la conexión con un cliente."""
    print(f"New client connected from {addr[0]}:{addr[1]}")

    try:
        message = receive_data(conn)

        if message:
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")

            response = process_message(message)
            conn.send(response.encode('utf-8'))
            print(f"Sent response to {addr}: {response}")

            if message[:3] == bytes([0x01, 0x02, 0x03]):
                print(f"Los bytes se correspondían con 0x01 0x02 0x03")
            else:
                print(f"Los bytes no se correspondían con 0x01 0x02 0x03")

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def process_message(message):
    """Procesa el mensaje recibido y devuelve la respuesta adecuada."""
    if message[0] == 0x01:
        return "mensaje de autenticación recibido"
    else:
        return "mensaje de datos recibido"
