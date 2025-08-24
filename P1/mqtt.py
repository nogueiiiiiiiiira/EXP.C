from machine import Pin, PWM
import network
from time import sleep
from umqtt.simple import MQTTClient
from hcsr04 import HCSR04

led = Pin(2, Pin.OUT)
buzzer = PWM(Pin(15))
buzzer.duty_u16(0)
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
parar = False

distancia_antiga = sensor.distance_cm()

# Configuração MQTT 
MQTT_CLIENT_ID = "ClienteID"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/espparapc"  
MQTT_TOPIC_RECEIVE = "exp.criativa/pcparaesp" 

# Configuração da rede Wi-Fi
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Função de callback para recebimento de mensagens MQTT
def callback(topic, msg):
    global parar
    print("Mensagem recebida: ", msg.decode())

    if msg.decode() == "parar":
        parar = True

# Conexão à rede Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
print("Conectado à rede Wi-Fi....")
while not wifi.isconnected():
    pass
print("Conectado à rede Wi-Fi:", WIFI_SSID)

# Configuração do cliente MQTT
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.set_callback(callback)

# Conexão e subscrição aos tópicos MQTT
client.connect()
client.subscribe(MQTT_TOPIC_RECEIVE)
print("Conectado ao broker MQTT...")

while not parar:
    client.check_msg()
    sleep(0.1)

    distancia_nova = sensor.distance_cm()

    print(f"Distância atual: {distancia_nova} cm")
    if distancia_nova - distancia_antiga > 20:
        print("Alteração de posição detectada!")
        client.publish(MQTT_TOPIC_SEND, "Alteracao de posicao detectada")

    distancia_antiga = distancia_nova

print("Parando leituras. Ligando LED e buzzer...")
for i in range(3):
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)

buzzer.freq(1000)
buzzer.duty_u16(32768)
sleep(2)
buzzer.duty_u16(0)

client.disconnect()
print("Código encerrado")