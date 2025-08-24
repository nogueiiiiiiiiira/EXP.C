import paho.mqtt.client as mqtt
from datetime import datetime
import time

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/pcparaesp"
MQTT_TOPIC_RECEIVE = "exp.criativa/espparapc"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    mensagem = msg.hora_minuto.decode()
    print("Pedido recebido:", mensagem)

    if mensagem == "hora":
        agora = datetime.now()
        hora = agora.hour
        minuto = agora.minute
        hora_minuto = f"{hora},{minuto}"
        print("Enviando:", hora_minuto)
        client.publish(MQTT_TOPIC_SEND, hora_minuto)

# Configuração do cliente MQTT
client = mqtt.Client("ClienteID")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Servidor de horas rodando...")
client.loop_forever()
