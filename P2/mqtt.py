from machine import Pin, PWM
from time import sleep
import network
from umqtt.simple import MQTTClient

button = Pin(12, Pin.IN, Pin.PULL_UP) 
servo = PWM(Pin(13), freq=50)        

duty_min = 26   
duty_max = 128 

def definir_angulo(angulo):
    duty = int(duty_min + (angulo / 180) * (duty_max - duty_min))
    servo.duty(duty)

# Configuração MQTT 
MQTT_CLIENT_ID = "ESP32_Client"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC_SEND = "exp.criativa/espparapc2025"  
MQTT_TOPIC_RECEIVE = "exp.criativa/pcparaesp2025" 

# Configuração da rede Wi-Fi
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    pass
print("Conectado ao Wi-Fi!")

# Função de callback para recebimento de mensagens MQTT
def callback(topic, msg):
    mensagem = msg.decode()
    print("Mensagem recebida:", mensagem)

    try:
        dados = dict(item.split("=") for item in mensagem.split(";"))
        ang_hora = int(dados["HORA"])
        ang_minuto = int(dados["MINUTO"])

        # Movimento
        definir_angulo(ang_hora)
        sleep(5)
        definir_angulo(ang_minuto)
        sleep(5)
        definir_angulo(0)

    except Exception as e:
        print("Erro no processamento:", e)

# Configuração do cliente MQTT
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.set_callback(callback)

# Conexão e subscrição aos tópicos MQTT
client.connect()
client.subscribe(MQTT_TOPIC_RECEIVE)
print("Conectado ao broker!")

# Loop
while True:
    client.check_msg()
    if not button.value():
        print("Botão pressionado! Solicitando hora...")
        client.publish(MQTT_TOPIC_SEND, "hora")
        sleep(0.5)
