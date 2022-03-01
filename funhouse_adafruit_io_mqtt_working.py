# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
from adafruit_funhouse import FunHouse

funhouse = FunHouse(default_bg=0x000000, scale=3)
funhouse.peripherals.set_dotstars(0x800000, 0x808000, 0x008000, 0x000080, 0x800080)

# Turn dotstars off
funhouse.peripherals.dotstars.fill(0)
funhouse.display.brightness = 0

TEMPERATURE_OFFSET = (
    4  # Degrees C to adjust the temperature to compensate for board produced heat
)

# create the labels
funhouse.display.show(
    None
)  # speed up display by not refreshing until all sensors are loaded
temp_label = funhouse.add_text(text="TEMP:", text_position=(1, 10), text_color=0xE5F20C)
humid_label = funhouse.add_text(
    text="HUMID:", text_position=(1, 30), text_color=0xE5F20C
)
pressure_label = funhouse.add_text(
    text="PRESSURE:", text_position=(1, 50), text_color=0xE5F20C
)

# pylint: disable=unused-argument
def connected(client):
    print("Connected to Adafruit IO! Subscribing...")
    client.subscribe("funhouse.temperature")
    client.subscribe("funhouse.humidity")
    client.subscribe("function.pressure")


def subscribe(client, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def disconnected(client):
    print("Disconnected from Adafruit IO!")


def message(client, feed_id, payload):
    print("Feed {0} received new value: {1}".format(feed_id, payload))
    if feed_id == "funhouse.temperature":
        if int(payload) == 1:
            funhouse.peripherals.play_tone(2000, 0.25)
    if feed_id == "funhouse.humidity":
        print(payload)
        color = int(payload[1:], 16)
        funhouse.peripherals.dotstars.fill(color)


# pylint: enable=unused-argument

# Initialize a new MQTT Client object
funhouse.network.init_io_mqtt()
funhouse.network.on_mqtt_connect = connected
funhouse.network.on_mqtt_disconnect = disconnected
funhouse.network.on_mqtt_subscribe = subscribe
funhouse.network.on_mqtt_message = message

print("Connecting to Adafruit IO...")
funhouse.network.mqtt_connect()
sensorwrite_timestamp = time.monotonic()
last_pir = None

while True:
    funhouse.network.mqtt_loop()

    print("Temp %0.1F" % (funhouse.peripherals.temperature - TEMPERATURE_OFFSET))
    print("Pres %d" % funhouse.peripherals.pressure)
    print("Humid %0.0F" % funhouse.peripherals.relative_humidity)
    # refresh sensor data and display on screen inside the loop function
    funhouse.display.brightness = 0.3
    funhouse.set_text(
        "Temp:%0.1F C" % (funhouse.peripherals.temperature - TEMPERATURE_OFFSET),
        temp_label,
    )
    funhouse.set_text(
        "Humid:%.0F %% rH" % funhouse.peripherals.relative_humidity, humid_label
    )
    funhouse.set_text("Baro:%.0F hPa" % funhouse.peripherals.pressure, pressure_label)
    funhouse.display.show(funhouse.splash)  # Displays all the sensor data on display
    time.sleep(1)
    funhouse.display.show(None)  # Clear the screen

    # every 300 seconds, write temp/hum/press
    if (time.monotonic() - sensorwrite_timestamp) > 30:
        funhouse.peripherals.led = True
        print("Sending data to adafruit IO!")
        funhouse.network.mqtt_publish(
            "funhouse.temperature", funhouse.peripherals.temperature
        )
        funhouse.network.mqtt_publish(
            "funhouse.humidity", int(funhouse.peripherals.relative_humidity)
        )
        funhouse.network.mqtt_publish(
            "funhouse.pressure", int(funhouse.peripherals.pressure)
        )
        sensorwrite_timestamp = time.monotonic()
        # Send PIR only if changed!
        if last_pir is None or last_pir != funhouse.peripherals.pir_sensor:
            last_pir = funhouse.peripherals.pir_sensor
            funhouse.network.mqtt_publish("pir", "%d" % last_pir)
        funhouse.peripherals.led = False
