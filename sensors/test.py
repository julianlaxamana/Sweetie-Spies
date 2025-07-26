import machine
import dht
from time import sleep
import utime
from machine import Pin, ADC
import network
import mqtt

ssid = 'Hotspot'
password = 'Storebucks123'
MQTT_SERVER = b'c2eae9532fbe4dd8b4079236e26d4f25.s1.eu.hivemq.cloud'
MQTT_SSL_PARAMS = {'server_hostname': MQTT_SERVER}
MQTT_USER = 'sweetiepies'
MQTT_PASS = 'Hack2025'

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

client = mqtt.MQTTClient("pico", MQTT_SERVER, port=8883, user=MQTT_USER, password=MQTT_PASS, ssl=True, ssl_params=MQTT_SSL_PARAMS)

client.connect()
#Pin GP-16 was used for temp/humidity sensor
sensor = dht.DHT11(machine.Pin(16))


# Set up ADC on GPIO 26
ldr = ADC(Pin(26))


# Define the trigger and echo pins

#trig pin is 14, echo is 15, power, and ground
TRIG_PIN = 14
ECHO_PIN = 15
trigger = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def measure_distance():
    """
    Measures the distance to an object using an ultrasonic sensor.

    Returns:
        float: The distance in centimeters, or None if the reading times out.
    """
    # Ensure trigger is low
    trigger.low()
    utime.sleep_us(2)
    
    # Trigger the sensor (10us pulse)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    # Wait for the echo to start
    while echo.value() == 0:
        pass
    start_time = utime.ticks_us()
    
    # Wait for the echo to end
    while echo.value() == 1:
        pass
    end_time = utime.ticks_us()
    
    # Calculate the duration and distance
    duration = utime.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2  # Speed of sound = 343m/s, converted to cm/us
    return distance




def read_light():
    # Read ADC value (0-65535 for 16-bit ADC)
    adc_value = ldr.read_u16()
    
    # Convert to voltage (0-3.3V)
    voltage = adc_value * 3.3 / 65535
    
    # Calculate LDR resistance
    if voltage < 3.3:
        ldr_resistance = 3000 * voltage / (3.3 - voltage)
    else:
        ldr_resistance = float('inf')
    
    # Convert to "lumens" scale (adjusted to your preference)
    if ldr_resistance > 0:
        lumens = 50.5 / ldr_resistance
    else:
        lumens = 0
    
    print(f"Light: {lumens:.2f} lumens")
    return lumens
    
def main():
    """
    Main function to continuously measure and print the distance.
    """
    while True:
        distance = measure_distance()
        if distance:
            print("Distance: {:.2f} cm".format(distance))
        light = read_light()
        sensor.measure()
        temp_c = sensor.temperature()
        temp_f = (temp_c * 9 / 5) + 32 - 6.6
        humidity = sensor.humidity() + 15
        client.publish("temp", str(temp_f))
        client.publish("humidity", str(humidity))
        client.publish("ultrasonic", str(distance))
        client.publish("light", str(light))
        print("Temp: ", temp_f, "Humidity: ", humidity)
        print (" ")
        sleep(3)


if __name__ == "__main__":
    main()

1