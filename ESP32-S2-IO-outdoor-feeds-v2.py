# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
# Adapted from https://learn.adafruit.com/adafruit-esp32-s2-feather/i2c-on-board-sensors

import board
from adafruit_ms8607 import MS8607
import alarm
import time
import neopixel
import digitalio
import adafruit_requests

# Setup MMQT service from ESP32-S2-internet-test.py example script
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from adafruit_lc709203f import LC709203F, PackSize

try:
    from secrets import secrets
except ImportError:
    print("WiFi and Adafruit IO credentials are kept in secrets.py, please add them there!")
    raise


# Duration of sleep in seconds. Default is 600 seconds (10 minutes).
# Feather will sleep for this duration between sensor readings / sending data to AdafruitIO
sleep_duration = 600

# Update to match the mAh of your battery for more accurate readings.
# Can be MAH100, MAH200, MAH400, MAH500, MAH1000, MAH2000, MAH3000.
# Choose the closest match. Include "PackSize." before it, as shown.
battery_pack_size = PackSize.MAH500

# Create i2c instance of sensor
i2c = board.I2C()
sensor = MS8607(i2c)
battery_monitor = LC709203F(board.I2C())
battery_monitor.pack_size = battery_pack_size

# Pull the I2C power pin low
i2c_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
i2c_power.switch_to_output()
i2c_power.value = False

# Create instance of Neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

# Collect the sensor data values and format the data
temperature = "{:.2f}".format(sensor.temperature)
temperature_f = "{:.2f}".format((sensor.temperature * (9 / 5) + 32))  # Convert C to F
humidity = "{:.2f}".format(sensor.relative_humidity)
pressure = "{:.2f}".format(sensor.pressure)
battery_voltage = "{:.2f}".format(battery_monitor.cell_voltage)
battery_percent = "{:.1f}".format(battery_monitor.cell_percent)

def go_to_sleep(sleep_period):
    # Create a an alarm that will trigger sleep_period number of seconds from now.
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_period)
    # Exit and deep sleep until the alarm wakes us.
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)


# Fetch the feed of the provided name. If the feed does not exist, create it.
def setup_feed(feed_name):
    try:
        # Get the feed of provided feed_name from Adafruit IO
        return io.get_feed(feed_name)
    except AdafruitIO_RequestError:
        # If no feed of that name exists, create it
        return io.create_new_feed(feed_name)

# Send the data. Requires a feed name and a value to send.
def send_io_data(feed, value):
    return io.send_data(feed["key"], value)

# Wi-Fi connections can have issues! This ensures the code will continue to run.
try:
    # Connect to Wi-Fi
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected to {}!".format(secrets["ssid"]))
    print("IP:", wifi.radio.ipv4_address)

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Wi-Fi connectivity fails with error messages, not specific errors, so this except is broad.
except Exception as e:  # pylint: disable=broad-except
    print(e)
    go_to_sleep(300)

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

# Turn on Neopixel when data is sent
pixel.fill((255, 0, 255))

# Print data values to the serial console. Not necessary for Adafruit IO.
print("Current sensor temperature: {0} C".format(temperature))
print("Current sensor temperature: {0} F".format(temperature_f))
print("Current sensor humidity: {0} %".format(humidity))
print("Current sensor pressure: {0} hPa".format(pressure))
print("Current battery voltage: {0} V".format(battery_voltage))
print("Current battery percent: {0} %".format(battery_percent))

# Adafruit IO sending can run into issues if the network fails!
# This ensures the code will continue to run.
try:
    print("Sending data to AdafruitIO...")
    # Send data to Adafruit IO
    # Create + New Group then +New Feed with the Name and Key of the feed
    send_io_data(setup_feed("feather.sensor-temperature"), temperature)
    send_io_data(setup_feed("feather.sensor-temperature-f"), temperature_f)
    send_io_data(setup_feed("feather.sensor-humidity"), humidity)
    send_io_data(setup_feed("feather.sensor-pressure"), pressure)
    send_io_data(setup_feed("feather.battery-voltage"), battery_voltage)
    send_io_data(setup_feed("feather.battery-percent"), battery_percent)
    print("Data sent!")
    # Turn off the Neopixel to indicate data sending is complete.
    pixel.fill((0,0,0))

# Adafruit IO can fail with multiple errors depending on the situation, so this except is broad.
except Exception as e:  # pylint: disable=broad-except
    print(e)
    go_to_sleep(300)

go_to_sleep(sleep_duration)
