# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_ms8607 import MS8607
import alarm
import time
import neopixel

# Setup MMQT service from ESP32-S2-internet-test.py example script
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from adafruit_lc709203f import LC709203F, PackSize

# Create i2c instance of sensor
i2c = board.I2C()
sensor = MS8607(i2c)

### WiFi ###

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
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
    client.subscribe("humidity")
    client.subscribe("temperature")
    client.subscribe("pressure")


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


# Create instance of Neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

humidity = sensor.relative_humidity
temperature = sensor.temperature
pressure = sensor.pressure
print("Publishing a new message every 30 seconds...")
print("Publishing {0}, {1}, {2} to outdoor sensor feed.".format(temperature, humidity, pressure))
io.publish("outdoor-sensor.humidity", humidity)
io.publish("outdoor-sensor.temperature", temperature)
io.publish("outdoor-sensor.pressure", pressure)

print("Pressure: %.2f hPa" % sensor.pressure)
print("Temperature: %.1f C" % sensor.temperature)
print("Humidity: %.2f %% rH" % sensor.relative_humidity)
print("\n------------------------------------------------\n")
#print((sensor.relative_humidity, sensor.temperature))
pixel.fill((255, 0, 255))
time.sleep(0.5)


# Create a an alarm that will trigger 30 seconds from now.
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 30)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
# Write your code here :-)