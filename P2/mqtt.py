from machine import Pin, PWM
from time import sleep
import network
from umqtt.simple import MQTTClient

button = Pin(12, Pin.IN, Pin.PULL_UP) 
servo = PWM(Pin(13), freq=50)        

# Configuração MQTT 
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_RECEIVE = "esp32/hora"
MQTT_TOPIC_SEND = "esp32/pedido"

# Configuração da rede Wi-Fi
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

def servo_angulo(angulo):

    duty = int(((angulo / 180) * 102) + 26) 
    servo.duty(duty)

# Função de callback para recebimento de mensagens MQTT
def callback(topic, msg):
    dados = msg.decode().split(",")
    hora = int(dados[0])
    minuto = int(dados[1])
    print("Hora recebida:", hora, "Minuto:", minuto)

    # mover para hora*7
    servo_angulo(hora * 7)
    sleep(5)

    # mover para minuto*7
    servo_angulo(minuto * 7)
    sleep(5)

    # voltar para 0
    servo_angulo(0)

# Conexão à rede Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    pass
print("Conectado ao Wi-Fi!")

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

    if button.value() == 0:
        print("Botão pressionado, pedindo hora...")
        client.publish(MQTT_TOPIC_SEND, "hora")
        sleep(1)
