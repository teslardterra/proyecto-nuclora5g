import sqlite3


# Conexión y creación de la base de datos
conn = sqlite3.connect('SubscribersLoRa.db')
c = conn.cursor()

# Crear tabla con los campos especificados
c.execute('''CREATE TABLE IF NOT EXISTS SuscribersLoRa
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              DeviceID BLOB NOT NULL UNIQUE, 
              PSK BLOB NOT NULL,             
                       
              Registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
              SessionDuration INTEGER)''')    

conn.close()
