from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def derivar_clave(cadena1, cadena2, nonce, longitud_clave=32):
    # Convierte las tuplas de enteros a bytes y luego combina
    combinacion = bytes(cadena1) + bytes(cadena2) + nonce
    
    # Utiliza PBKDF2 para derivar una clave de longitud especificada
    clave = PBKDF2(combinacion, nonce, dkLen=longitud_clave)
    
    return clave

# Ejemplo de uso
cadena1 = (0x01, 0x02)
cadena2 = (0x04, 0x03)
nonce = bytes.fromhex("12")  # Convertir nonce a bytes (es de un solo byte)

clave_derivada = derivar_clave(cadena1, cadena2, nonce)
print(f"La clave derivada es: {clave_derivada.hex()}")

