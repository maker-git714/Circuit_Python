# SPDX-FileCopyrightText: 2020 by Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# using Feather ESP32-S2 with SGP40 and AHT20 sensors to send environmental data
# to AdafruitIO

import time
import board
import adafruit_ahtx0
import adafruit_sgp40

import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

# Boards i2c bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
aht = adafruit_ahtx0.AHTx0(i2c)

### WiFi ###

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

# Define callback functions which will be called when certain events happen.
# pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print("Connected to Adafruit IO!  Listening for Feed changes...")
    # Subscribe to changes on feeds.
    client.subscribe("SensorFeed")
    client.subscribe("temperature")
    client.subscribe("humidity")

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))

# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")


# pylint: disable=unused-argument
def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print("Feed {0} received new value: {1}".format(feed_id, payload))


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to Adafruit IO
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe
io.on_unsubscribe = unsubscribe
io.on_message = message

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

counter = 0

while True:
    temperature = aht.temperature
    humidity = aht.relative_humidity

    # For compensated raw gas readings
    compensated_raw_gas = sgp.measure_raw(temperature, humidity)

    # For Compensated voc index readings
    # The algorithm expects a 1 hertz sampling rate. Run "measure index" once per second.
    # It may take several minutes for the VOC index to start changing
    # as it calibrates the baseline readings.
    voc_index = sgp.measure_index(temperature=temperature, relative_humidity=humidity)

    print("Raw Data:", compensated_raw_gas)
    print("VOC Index:", voc_index)
    print("Temperature = %0.1f C" % aht.temperature)
    print("Humidity = %0.0f %%" % aht.relative_humidity)
    #print((voc_index,))
    print("")
    time.sleep(1)

    if counter == 3:
        value1 = voc_index
        value2 = temperature
        value3 = humidity
        print("Publishing a new message every 5 seconds...")
        print("Publishing {0} to SensorFeed." .format(value1))
        io.publish("SensorFeed", value1)
        io.publish("temperature", value2)
        io.publish("humidity", value3)
        counter = 0
    else:
        counter +=1
