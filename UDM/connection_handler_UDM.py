from utils_UDM import receive_data, identify_connection, send_bytes
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
        
        if(conn_client_name == "AMF"):
            fla_identifier = b'\x97'
            message = message[:-1]  + fla_identifier
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")
            print(f"Asking UDR to check DeviceID")
            
            # Conectar al UDR
            conn_UDR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_UDR.connect(tuple(addresses["UDR"]))           

            if send_bytes(conn_UDR, message):
              response = receive_data(conn_UDR)
              conn_UDR.close()

              if response.decode('utf-8') == "FLA SUCCESS":
                print(f"[UDM] [FLA] FLA SUCCESS")
                conn.send(response) #Devuelta al AMF

              elif response.decode('utf-8') == "FLA FAILURE":
                print(f"[UDM] [FLA] FLA FAILURE")
                conn.send(response) #Devuelta al AMF

        elif(conn_client_name == "AUSF"):
           sla_identifier = b'\x98'
           message = message[:-1]  + sla_identifier
           print(f"Received message from {addr} (hex): {message.hex()}")
           print(f"Received message from {addr} (decimal): {list(message)}")
           print(f"Asking UDR to retrieve SLA data")
           # Conectar al UDR
           conn_UDR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           conn_UDR.connect(tuple(addresses["UDR"]))           

           if send_bytes(conn_UDR, message):
            response = receive_data(conn_UDR)
            conn_UDR.close()
            print("[SLA] Returning authentication data to AUSF")

            conn.send(response) #Devuelta al AUSF
        
        elif(conn_client_name == "SMF"):
           to_store_transmission_identifier = b'\x99'
           message = message[:-1]  + to_store_transmission_identifier
           print(f"Received message from {addr} (hex): {message.hex()}")
           print(f"Received message from {addr} (decimal): {list(message)}")
           print(f"Asking UDR to store transmission data")
           # Conectar al UDR
           conn_UDR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           conn_UDR.connect(tuple(addresses["UDR"]))           

           if send_bytes(conn_UDR, message):
            response = receive_data(conn_UDR)
            conn_UDR.close()
            print("[STORE] Data received and stored by UDR")

            conn.send(response) #Respuesta al UDR
            
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

    