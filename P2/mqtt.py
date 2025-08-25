from machine import Pin, PWM
from time import sleep
import network
from umqtt.simple import MQTTClient

button = Pin(12, Pin.IN, Pin.PULL_UP) 
servo = PWM(Pin(13), freq=50)        

# Configuração MQTT 
MQTT_CLIENT_ID = "ClienteID"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/espparapc2025"  
MQTT_TOPIC_RECEIVE = "exp.criativa/pcparaesp2025" 

# Configuração da rede Wi-Fi
WIFI_SSID = "Visitantes"
WIFI_PASS = ""

# Conexão à rede Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    pass
print("Conectado ao Wi-Fi!")

# Função de callback para recebimento de mensagens MQTT
def callback(topic, msg):
    print("Mensagem recebida: ", msg.decode())

# Configuração do cliente MQTT
client = MQTTClient("ClientID", MQTT_BROKER)
client.set_callback(callback)

# Conexão e subscrição aos tópicos MQTT
client.connect()
client.subscribe(MQTT_TOPIC_RECEIVE)
print("Conectado ao broker!")


while True:
    client.check_msg()
    sleep(0.1)

    client.publish(MQTT_TOPIC_SEND, "hora")
    client.check_msg()
    #callback(MQTT_TOPIC_RECEIVE, msg)
