import sqlite3

# Conexión y creación de la base de datos
conn = sqlite3.connect('SessionsLoRa.db')
c = conn.cursor()

# Crear tabla con los campos especificados
c.execute('''CREATE TABLE IF NOT EXISTS SessionsLoRa
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              DeviceID BLOB NOT NULL,          
              SessionNonce BLOB NOT NULL, 
              DerivationNonce BLOB NOT NULL,          
              SessionDuration INTEGER,         
              SessionCounter INTEGER,         
              SessionDerivatedKey BLOB NOT NULL)''')  

# Ejemplo de inserción de datos
try:
    # Convertir los campos a bytes
   # device_id = bytes([0x01, 0x02, 0x03])       # DeviceID de 3 bytes
   # session_nonce = bytes([0xAA, 0xBB])         # SessionNonce de 2 bytes
    #session_duration = 3600                     # Duración de la sesión en segundos (1 hora)
    #session_counter = 1                         # Contador de sesiones
   # session_derivated_key = bytes([0xFF] * 32)  # Clave derivada de 32 bytes (ejemplo: todos los bytes son 0xFF)

    #Ejemplo Insertar datos
    #c.execute("INSERT INTO SessionsLoRa (DeviceID, SessionNonce, SessionDuration, SessionCounter, SessionDerivatedKey) VALUES (?, ?, ?, ?, ?)",
     #         (device_id, session_nonce, session_duration, session_counter, session_derivated_key))

    # Guardar cambios
    #conn.commit()
    print("Base creada correctamente.")
except sqlite3.IntegrityError:
    print("Error: Violación de integridad (por ejemplo, clave duplicada).")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    # Cerrar conexión
    conn.close()