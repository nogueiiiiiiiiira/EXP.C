import paho.mqtt.client as mqtt

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/pcparaesp"
MQTT_TOPIC_RECEIVE = "exp.criativa/espparapc"

# Callback executado quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print(f"Mensagem recebida no tópico")
    
    if mensagem == "Alteracao de posicao detectada":
        print("Objeto mudou de posição!")
        
        client.publish(MQTT_TOPIC_SEND, "parar")
        print("Comando de parar enviado para ESP.")

# Configuração do cliente MQTT
client = mqtt.Client("ClienteID")
client.on_message = on_message

# Conexão ao broker MQTT e subscrição aos tópicos
client.connect(MQTT_BROKER)
client.subscribe(MQTT_TOPIC_RECEIVE)

print("Esperando mensagens...")
client.loop_forever()