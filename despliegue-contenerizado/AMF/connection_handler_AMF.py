from utils_AMF import receive_data, identify_connection, send_bytes
import socket
def handle_client(conn, addr, addresses):
    """Maneja la conexión con un cliente."""
    "addr es la ip del cliente que se conecta"
    "addresses es el diccionario con las distintas ips que manda el NRF"

    print(f"New client connected from {addr[0]}:{addr[1]}")

    
    try:
        message = receive_data(conn)
        conn_client_name = identify_connection(message)
        print(f"Connection identified as: {conn_client_name}")  

        # Modificar el último byte del mensaje como identificador del SMF
        amf_identifier = b'\x03'  # Puedes cambiar este valor según sea necesario
        message = message[:-1] + amf_identifier
        
        if(conn_client_name == "SMF"):
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")
            response = "ACK FROM AMF"
            conn.send(response.encode('utf-8'))
            
            print("Starting first level authentication check...")
            # Conectar al UDM
            conn_UDM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_UDM.connect(tuple(addresses["UDM"]))            

            # Crear un nuevo mensaje con el segundo, tercer y cuarto byte de message
            deviceID = message[1:4]  #bytes: 2,3,4  - deviceID
            FLA_message = deviceID + amf_identifier

            print("[AMF] [FLA] Sending message to UDM")

            if send_bytes(conn_UDM, FLA_message):
              response = receive_data(conn_UDM)
              
              if response.decode('utf-8') == "FLA SUCCESS":
                print(f"[UDM] [FLA] FLA SUCCESS")
                # Conectar al UDM
                conn_AUSF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn_AUSF.connect(tuple(addresses["AUSF"]))   
                print(f"Redirecting authentication message to AUSF")

                if send_bytes(conn_AUSF, message):
                  response = receive_data(conn_AUSF)
                  if response:
                     print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                  conn_AUSF.close()

              
              elif response.decode('utf-8') == "FLA FAILURE":
                print(f"[UDM] [FLA] FLA FAILURE")

              conn_UDM.close()

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

    