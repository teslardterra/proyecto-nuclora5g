import sqlite3
import datetime

# Conexión y creación de la base de datos
conn = sqlite3.connect('TransmissionsLoRa.db')
c = conn.cursor()

# Crear tabla con los campos especificados y restricción de unicidad en DeviceID
c.execute('''CREATE TABLE IF NOT EXISTS TransmissionsLoRa
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              DeviceID BLOB NOT NULL,  
              Received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              Received_data BLOB,
              Data_type BLOB NOT NULL)''')  

# Ejemplo de inserción de datos
try:
    # Convertir el DeviceID a bytes (3 bytes)
    device_id = bytes([0x01, 0x02, 0x03])  # Ejemplo de DeviceID
    received_data = bytes([0xFF, 0xEE, 0xDD, 0xCC])  # Ejemplo de datos recibidos
    data_type = bytes([0x01])  # Ejemplo de Data_type como bytes

    # Insertar datos
    c.execute("INSERT INTO TransmissionsLoRa (DeviceID, Received_at, Received_data, Data_type) VALUES (?, ?, ?, ?)",
              (device_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), received_data, data_type))

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