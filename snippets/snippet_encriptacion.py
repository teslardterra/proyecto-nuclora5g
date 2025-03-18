from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

def chacha20_encrypt(data: bytes, key: str, nonce_number: int) -> bytes:
    """
    Encripta datos en bytes usando ChaCha20.
    
    :param data: Bytes a encriptar.
    :param key: Clave en formato hexadecimal.
    :param nonce_number: Nonce como número entero.
    :return: Bytes encriptados.
    """
    key = bytes.fromhex(key)[:32]  # Asegurar 32 bytes de clave
    nonce = nonce_number.to_bytes(16, 'big')  # Convertir número a 16 bytes

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_data = encryptor.update(data)
    
    return encrypted_data

def chacha20_decrypt(encrypted_data: bytes, key: str, nonce_number: int) -> bytes:
    """
    Desencripta datos en bytes usando ChaCha20.
    
    :param encrypted_data: Bytes encriptados.
    :param key: Clave en formato hexadecimal.
    :param nonce_number: Nonce como número entero.
    :return: Bytes desencriptados.
    """
    key = bytes.fromhex(key)[:32]
    nonce = nonce_number.to_bytes(16, 'big')

    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(encrypted_data)
    
    return decrypted_data


# Ejemplo de uso
clave = "589aa2821629785891caea8dabf657b614dd4527992c4fb9be485179e85b9f6f"
nonce = 12  # Nonce como número entero

# Array de 51 bytes
array_bytes = bytearray([i for i in range(51)])  # Ejemplo: array de bytes del 0 al 50

# Seleccionar los bytes que deseas encriptar (por ejemplo, del índice 0 al 3)
start_index = 0
end_index = 2  # Ahora end_index es inclusivo
bytes_a_encriptar = array_bytes[start_index:end_index + 1]  # Usamos end_index + 1

# Encriptar los bytes seleccionados
bytes_encriptados = chacha20_encrypt(bytes_a_encriptar, clave, nonce)

# Reemplazar los bytes originales en el array con los bytes encriptados
array_bytes[start_index:end_index + 1] = bytes_encriptados  # Usamos end_index + 1

# Mostrar el array de bytes modificado
print("Array de bytes modificado (encriptado):", array_bytes.hex())

# Desencriptar los bytes encriptados
bytes_desencriptados = chacha20_decrypt(bytes_encriptados, clave, nonce)

# Reemplazar los bytes encriptados en el array con los bytes desencriptados
array_bytes[start_index:end_index + 1] = bytes_desencriptados  # Usamos end_index + 1

# Mostrar el array de bytes restaurado
print("Array de bytes restaurado (desencriptado):", array_bytes.hex())