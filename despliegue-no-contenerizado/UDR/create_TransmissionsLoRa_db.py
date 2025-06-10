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


conn.close()