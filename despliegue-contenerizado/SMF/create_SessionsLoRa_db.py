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

conn.close()