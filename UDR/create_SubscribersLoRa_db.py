import sqlite3


# Conexión y creación de la base de datos
conn = sqlite3.connect('SubscribersLoRa.db')
c = conn.cursor()

# Crear tabla con los campos especificados
c.execute('''CREATE TABLE IF NOT EXISTS SuscribersLoRa
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              DeviceID BLOB NOT NULL UNIQUE, 
              PSK BLOB NOT NULL,             
              PSCC BLOB NOT NULL,             
              Registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
              SessionDuration INTEGER)''')    

# Ejemplo de inserción de datos
try:
    # Convertir los campos a bytes
    device_id = bytes([0x01, 0x02, 0x03])  # DeviceID de 3 bytes
    psk = bytes([0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13])  # PSK de 16 bytes
    pscc = bytes([0xAA, 0xBB, 0xCC])       # PSCC de 3 bytes
    session_duration = 30000  # Duración de la sesión en segundos (1 hora)

    # Insertar datos (Registered_at se genera automáticamente)
    c.execute("INSERT INTO SuscribersLoRa (DeviceID, PSK, PSCC, SessionDuration) VALUES (?, ?, ?, ?)",
              (device_id, psk, pscc, session_duration))

    # Guardar cambios
    conn.commit()
    print("Datos insertados correctamente.")
except sqlite3.IntegrityError:
    print("Error: El DeviceID ya existe en la base de datos.")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    # Cerrar conexión
    conn.close()