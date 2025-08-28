import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/pcparaesp2025"
MQTT_TOPIC_RECEIVE = "exp.criativa/espparapc2025"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    data_hora = datetime.now()
    horas = data_hora.hour
    minutos = data_hora.minute

    ang_hora = horas * 7
    ang_minuto = minutos * 7

    mensagem = msg.payload.decode()
    print(f"Mensagem recebida: {mensagem}")
    
    if mensagem == "hora":
        pedido = f"HORA = {ang_hora}; MINUTO = {ang_minuto}"
        client.publish(MQTT_TOPIC_SEND, pedido)
        print("Angulos enviados:", pedido)

# Configuração do cliente MQTT
client = mqtt.Client("ClienteID")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Esperando mensagens...")

while True:
    client.loop(timeout=0.1)import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/pcparaesp2025"
MQTT_TOPIC_RECEIVE = "exp.criativa/espparapc2025"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    data_hora = datetime.now()
    horas = data_hora.hour
    minutos = data_hora.minute

    ang_hora = horas * 7
    ang_minuto = minutos * 7

    mensagem = msg.payload.decode()
    print(f"Mensagem recebida: {mensagem}")
    
    if mensagem == "hora":
        pedido = f"HORA = {ang_hora}; MINUTO = {ang_minuto}"
        client.publish(MQTT_TOPIC_SEND, pedido)
        print("Angulos enviados:", pedido)

# Configuração do cliente MQTT
client = mqtt.Client("ClienteID")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Esperando mensagens...")

while True:
    client.loop(timeout=0.1)
