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

def return_addresses():
    """Temporal, retorna direcciones del resto de componentes"""
    ADDR_UPF = ("192.168.70.134", 5051)
    ADDR_SMF = ("192.168.70.136", 5052)
    ADDR_AMF = ("192.168.70.138", 5053)
    ADDR_AUSF = ("192.168.70.135", 5054)
    ADDR_UDM = ("192.168.70.133", 5055)
    ADDR_UDR = ("192.168.70.137", 5056)

    addresses = {
        "UPF": ADDR_UPF,
        "SMF": ADDR_SMF,
        "AMF": ADDR_AMF,
        "AUSF": ADDR_AUSF,
        "UDM": ADDR_UDM,
        "UDR": ADDR_UDR
    }
    return addresses