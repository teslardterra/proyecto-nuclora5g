import paho.mqtt.client as mqtt
import logging
import json
import socket

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes de conexión MQTT
BROKER_URL = "eu1.cloud.thethings.network"
BROKER_PORT = 1883
TOPIC = "v3/loranero@ttn/devices/+/up"
USERNAME = "loranero@ttn"
PASSWORD = "NNSXS.5GGQYVB2T5CUN4Q6JZ3Q3R2WCOZMQTJRSMQUZ5Y.RESRY7H4YKWWUJCOHPSKIFG4VDDI7N6W37BHS4L4IFFKMKDGSEMA"

# Configuración de destino TCP
TCP_IP = "192.168.70.134"
TCP_PORT = 5568
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
        print(payload_dict)

        send_to_tcp_server(payload_dict)
    except Exception as e:
        logging.error(f"Error al procesar el mensaje: {e}")

def on_log(client, userdata, level, buf):
    logging.debug(buf)

# Enviar datos a un servidor TCP
def send_to_tcp_server(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(TCP_ADDR)
            json_data = json.dumps(data)
            sock.send(json_data.encode("utf-8"))
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
