import socket

def receive_data(conn, buffer_size=1024):
    """
    Recibe datos del servidor.
    :param conn: El objeto de conexión del servidor.
    :param buffer_size: Tamaño del búfer para recibir datos.
    :return: Los datos recibidos como bytes, o None si no se recibieron datos.
    """
    try:
        data = conn.recv(buffer_size)
        return data if data else None
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None




def resolve(name, port):
    """Resuelve el nombre del contenedor a una IP actual en Docker."""
    try:
        ip = socket.gethostbyname(name)
        return (ip, port)
    except socket.gaierror:
        print(f"[ERROR] No se pudo resolver: {name}")
        return None


def return_addresses():
    """Resuelve dinámicamente las direcciones IP de los componentes."""
    addresses = {
        "UPF": resolve("oai-upf", 5051),
        "SMF": resolve("oai-smf", 5052),
        "AMF": resolve("oai-amf", 5053),
        "AUSF": resolve("oai-ausf", 5054),
        "UDM": resolve("oai-udm", 5055),
        "UDR": resolve("oai-udr", 5056)
    }
    return addresses


