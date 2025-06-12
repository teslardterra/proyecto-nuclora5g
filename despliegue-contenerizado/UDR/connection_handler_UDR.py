from utils_UDR import receive_data, FLA_check_DeviceID, SLA_retrieve_data, derive_key, store_transmission
import time
def handle_client(conn, addr):
    """Maneja la conexión con un cliente."""
    "addr es la ip del cliente que se conecta"
    "addresses es el diccionario con las distintas ips que manda el NRF"

    print(f"New client connected from {addr[0]}:{addr[1]}")

    
    try:
        message = receive_data(conn) 
        

        if message[-1] == 0x97:
          message = message[:-1]

          print(f"[UDR] [FLA] Checking DeviceID")
          result = FLA_check_DeviceID(message)

          if result:
            print(f"[UDR] [FLA] DeviceID found in subscribers database")
            print(f"[UDR] [FLA] SUCCESS")
            response = "FLA SUCCESS"
            conn.send(response.encode('utf-8'))

          else:
            print(f"[UDR] [FLA] DeviceID not found in database")
            print(f"[UDR] [FLA] FAILURE")
            response = "FLA FAILURE"
            conn.send(response.encode('utf-8'))

        elif message[-1] == 0x98:
           message = message[:-1]
           retrieved_data = SLA_retrieve_data(message)
           DeviceID = message[:3]
           derivation_nonce = message[3:4]
           PSK = retrieved_data[0]
          
           SessionDuration = retrieved_data[1]

           print(f"{PSK}")
           print(f"{SessionDuration}")
         
           
           key = derive_key(DeviceID, PSK, derivation_nonce)
     
           response = key + SessionDuration.to_bytes(2, 'big')
           
           print("[SLA] Returning authentication data to UDM")

           conn.send(response)

        elif message[-1] == 0x99:
            message = message[:-1]
            DeviceID = message[:3]
            data_type = message[3:4]
            data = message[4:]
            store_transmission(DeviceID, data_type, data)
            print(f"[UDR] Transmission stored")
            response = "ACK FROM UDR"
            conn.send(response.encode('utf-8'))
            final = time.time()

            # Guardar 'final' (fin de procesamiento de mensaje de datos correcto) en un archivo de texto, para pruebas
          # with open("final_tiempos.txt", "a") as f:
            #    f.write(f"{final}\n")

  
     
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

    
