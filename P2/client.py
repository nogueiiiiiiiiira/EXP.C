import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/pcparaesp2025"
MQTT_TOPIC_RECEIVE = "exp.criativa/espparapc2025"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    current_datetime = datetime.now()
    horas = (current_datetime.hour)
    minutos = (current_datetime.minute)
    segundos = (current_datetime.second)

    mensagem = msg.payload.decode()
    print(f"Mensagem recebida no tópico")
    
    if mensagem == "hora":        
        pedido = (f"{horas}:{minutos}:{segundos}")
        client.publish(MQTT_TOPIC_SEND, pedido)
        print("Datetime enviado!")

# Configuração do cliente MQTT
client = mqtt.Client("ClienteID")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Esperando mensagens...")

while True:
    client.loop(timeout=0.1)
