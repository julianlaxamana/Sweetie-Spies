from machine import Pin, I2C
import ssd1306
import mqtt
import network
from time import sleep


ssid = 'HAcK-Project-WiFi-1'
password = 'UCLA.HAcK.2024.Summer'
text = []

MQTT_SERVER = b'c2eae9532fbe4dd8b4079236e26d4f25.s1.eu.hivemq.cloud'
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}
MQTT_USER = 'sweetiepies'
MQTT_PASS = 'Hack2025'

def onCallback(topic, message):
    global text
    print(message)
    text.insert(0, message)
    
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')

connect()

# using default address 0x3C
i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

client = mqtt.MQTTClient("pico", MQTT_SERVER, port=8883, user=MQTT_USER, password=MQTT_PASS, ssl=True, ssl_params=MQTT_SSL_PARAMS)
client.set_callback(onCallback)
client.connect()
client.subscribe("display")
while True:
    client.check_msg()
    num = 0
    display.fill(0)
    for line in text:
        display.text(line, 0, num * 10, 1)
        num += 1
    display.show()
