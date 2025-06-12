from utils_SMF import receive_data, identify_connection, identify_payload_type, send_bytes, sessiondb_open_new_session, session_check_DeviceID
from utils_SMF import chacha20_decrypt, session_nonce_addone, update_and_check_session_counter, update_and_check_session_counter_lost_case
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
        smf_identifier = b'\x02'  # Puedes cambiar este valor según sea necesario
        message = message[:-1] + smf_identifier
        
        if(conn_client_name == "UPF"):
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")
            response = "ACK FROM SMF"
            conn.send(response.encode('utf-8'))
            
            payload_type = identify_payload_type(message)
            print(f"Payload type detected: {payload_type}")

            if payload_type == "Authentication":
                print("Processing authentication message...")
                print("Redirecting authentication message to AMF...")
         
                # Conectar al AMF
                conn_AMF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn_AMF.connect(tuple(addresses["AMF"]))

                print(f"Redirecting message to AMF")

                if send_bytes(conn_AMF, message):
                    response = receive_data(conn_AMF)
                    if response:
                        print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                        conn_AMF.close()
                                              
            elif payload_type == "Data":
                print("Processing data message...") 
                message = message[:-1]

                DeviceID = message[1:4] 
                result = session_check_DeviceID(DeviceID)
                if result:
                    print(f"Session found, checking session data...")
                    SessionNonce = result[2]
                    SessionNonce_int = int.from_bytes(SessionNonce, 'big')
                    SessionDerivationNonce = result[3]
                    SessionDuration = result[4]
                    SessionCounter = result[5]
                    SessionDerivatedKey = result[6]
                    encrypted_bytes = message[4:51]
                    
                                       
                    if len(SessionDerivatedKey) == 32:  # Ensure key length is valid for chacha20
                      
                        decrypted_message = chacha20_decrypt(encrypted_bytes, SessionDerivatedKey.hex(), int.from_bytes(SessionDerivationNonce, 'big'))  
                        decrypted_SessionNonce = decrypted_message[0:1]
                        decrypted_Data = decrypted_message[1:]
                        decrypted_SessionNonce_int = int.from_bytes(decrypted_SessionNonce, 'big')

                        print(f"Decrypted data: {decrypted_Data}")
                    else:
                        print("Invalid key size for chacha20 decryption")

                    if decrypted_SessionNonce_int == SessionNonce_int:
                        print(f"[SMF][Session verified], updating session counters and control data")
                        print(f"[SMF][Session verified], sending data to UDM to store")
                        
                        session_nonce_addone(DeviceID)
                        update_and_check_session_counter(DeviceID)

                        conn_UDM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        conn_UDM.connect(tuple(addresses["UDM"]))
                        payload_type = message[0:1]
                        message = DeviceID + payload_type + decrypted_Data + smf_identifier

                        if send_bytes(conn_UDM, message):
                         response = receive_data(conn_UDM)
                         if response:
                           print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                           conn_UDM.close()

                    else:
                        print(f"[SMF][Session verified] [NONCE NOT MATCHING, checking for possible lost of packets...]")
                        if(update_and_check_session_counter_lost_case(DeviceID, decrypted_SessionNonce)):
                           print(f"[SMF][Session verified] [PREVIOUS LOST PACKETS, SESSION DATA UPDATED] [SENDING CURRENT ONE TO UDR]")

                           conn_UDM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                           conn_UDM.connect(tuple(addresses["UDM"]))
                           payload_type = message[0:1]
                           message = DeviceID + payload_type + decrypted_Data + smf_identifier

                           if send_bytes(conn_UDM, message):
                            response = receive_data(conn_UDM)
                           if response:
                            print(f"Respuesta recibida del servidor (bytes): {response.decode('utf-8')}")
                            conn_UDM.close()


                        else:
                           print(f"[SMF][Session verified] [MESSAGE NOT RECOGNIZED, DISCARDED]")

     
                else:
                    print(f"Session not found, message discarded")

        
        elif(conn_client_name == "AUSF"):                
            print(f"Received message from {addr} (hex): {message.hex()}")
            print(f"Received message from {addr} (decimal): {list(message)}")
            response = "ACK FROM SMF"
            conn.send(response.encode('utf-8'))

            message = message[:-1]
            print(f"[SMF][SESSION] Opening session...")
            DeviceID = message[:3]
            key = message[3:35]
            session_nonce = message[35:36]
            session_duration = int.from_bytes(message[36:38], 'big')
            derivation_nonce = message[38:39]
          
            sessiondb_open_new_session(DeviceID, key, session_nonce, derivation_nonce, session_duration)

     
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

    