import paho.mqtt.client as mqtt
import logging
import json
import socket
import base64

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes de conexión MQTT
BROKER_URL = "eu1.cloud.thethings.network"
BROKER_PORT = 1883
TOPIC = "topico"
USERNAME = "mi_usuario"
PASSWORD = "mi_password"






def get_local_ip():
    """Obtiene la IP local asignada al contenedor dentro de la red Docker."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# Configuración de destino TCP
TCP_IP = get_local_ip()
TCP_PORT = 5051
TCP_ADDR = (TCP_IP, TCP_PORT)

# Funciones de callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        logging.error(f"Error de conexión. Código: {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    logging.info(f"Suscripción exitosa al topic. QoS: {granted_qos}")

def on_message(client, userdata, message):
    try:
        payload_dict = json.loads(message.payload.decode("utf-8"))
        logging.info(f"Mensaje recibido en el topic: {message.topic}")
        
        # Extraer el frm_payload codificado en Base64
        frm_payload_base64 = payload_dict['uplink_message']['frm_payload']
        
        # Decodificar el payload de Base64 a bytes
        payload_bytes = base64.b64decode(frm_payload_base64)
        logging.info(f"Payload decodificado (en bytes): {payload_bytes}")
        print("En hexadecimal:", payload_bytes.hex())
        # Enviar el array de bytes al servidor TCP
        send_to_tcp_server(payload_bytes)
        
    except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")

def on_log(client, userdata, level, buf):
    logging.debug(buf)

# Enviar datos a un servidor TCP
def send_to_tcp_server(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(TCP_ADDR)
            sock.send(data)  # Enviar los bytes directamente
            logging.info("Datos enviados al servidor TCP.")
    except socket.error as e:
        logging.error(f"Error de socket: {e}")

# Función principal
def main():
    logging.info("Iniciando cliente MQTT...")

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(USERNAME, PASSWORD)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_log = on_log

    mqtt_client.connect(BROKER_URL, BROKER_PORT, keepalive=60)

    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logging.info("Script detenido por el usuario")
        mqtt_client.disconnect()

if __name__ == '__main__':
    main()
