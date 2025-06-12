from utils_AUSF import receive_data, identify_connection, send_bytes, chacha20_decrypt, obtain_3_md5_bytes
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
        ausf_identifier = b'\x04'  # Puedes cambiar este valor según sea necesario
        message = message[:-1] + ausf_identifier
        
        if(conn_client_name == "AMF"):
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")
            response = "ACK FROM AUSF"
            conn.send(response.encode('utf-8'))
            
            print(f"Starting second level authentication check...")
            deviceID = message[1:4]  #bytes: 2,3,4  - deviceID
            derivation_nonce = message[4:5]
            SLA_message = deviceID + derivation_nonce + ausf_identifier
                        
            print("[AMF] [SLA] Sending message to UDM")
            # Conectar al UDM
            conn_UDM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn_UDM.connect(tuple(addresses["UDM"]))    
            
            if send_bytes(conn_UDM, SLA_message):
              response = receive_data(conn_UDM)
              print("[SLA] Authentication data received from UDM")
              print("[SLA] Checking SLA...")
              key = response[:32]
              session_duration = int.from_bytes(response[32:], 'big') 
              print(f"derivation_nonce: {derivation_nonce}")
              print(f"key: {key}")

              message = message[:-1]
              
              encrypted_bytes = message[5:9]
              decrypted_session_nonce_and_HICC = chacha20_decrypt(encrypted_bytes, key.hex(), int.from_bytes(derivation_nonce, 'big'))         
              decrypted_session_nonce = decrypted_session_nonce_and_HICC[0:1]
              decrypted_HICC = decrypted_session_nonce_and_HICC[1:4]
              print(f"Decrypted HICC: {decrypted_HICC}")
              
              message_for_hash = message[0:5] + decrypted_session_nonce  #El hash se realiza de los campos descifrados excepto el propio HICC
              
              if obtain_3_md5_bytes(message_for_hash[:6]) == decrypted_HICC:
                print("[SLA] SLA SUCCESS")
                # Conectar al SMF
                conn_SMF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn_SMF.connect(tuple(addresses["SMF"]))
                session_message = deviceID + key + decrypted_session_nonce + session_duration.to_bytes(2, 'big') + derivation_nonce + ausf_identifier
                
                if send_bytes(conn_SMF, session_message):
                   print(f"[AUSF] [SESSION] Session data sent to SMF")
                   response = receive_data(conn_SMF)
                   if response:
                      print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                      conn_SMF.close()

              else:
                print("[SLA] SLA FAILURE")
                

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

    