from machine import Pin, PWM
import network
from time import sleep
from umqtt.simple import MQTTClient
from hcsr04 import HCSR04

led = Pin(2, Pin.OUT)
buzzer = PWM(Pin(15))
buzzer.duty(0)
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
parar = False

distancia_antiga = sensor.distance_cm()

# Configuração MQTT 
MQTT_CLIENT_ID = "ClienteID"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/espparapc2025"  
MQTT_TOPIC_RECEIVE = "exp.criativa/pcparaesp2025" 

# Configuração da rede Wi-Fi
WIFI_SSID = "Visitantes"
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
    
    distancia_antiga = sensor.distance_cm()
    print(f"\nDistância atual: {distancia_antiga} cm")
    sleep(2)
    distancia_nova = sensor.distance_cm()
    
    sleep(2)
    
    diferenca = distancia_nova - distancia_antiga

    if diferenca > 20:
        client.publish(MQTT_TOPIC_SEND, "Alteracao de posicao detectada")
        print("\nAlteração de posição detectada! Diferença de cm foi de:", diferenca, "cm")
        sleep(5)
        client.check_msg()
        parar = True
        
    else:
        print("\nA nova posicao foi menor que a antiga posicao")

print("\nParando leituras. Ligando LED e buzzer...")

for i in range(3):
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)
    
buzzer.freq(500)
buzzer.duty(500)
sleep(2)
buzzer.duty(0)

client.disconnect()
print("\nCódigo encerrado")
