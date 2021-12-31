# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
from time import sleep
import board
from adafruit_ms8607 import MS8607
import adafruit_lis3dh
import digitalio

i2c = board.I2C()
sensor = MS8607(i2c)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:

    # Blink LED with each loop
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.5)

    print("Pressure: %.2f hPa" % sensor.pressure)
    print("Temperature: %.2f C" % sensor.temperature)
    print("Humidity: %.2f %% rH" % sensor.relative_humidity)
    print("\n------------------------------------------------\n")

    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.
    x, y, z = lis3dh.acceleration
    print('x = {}G, y = {}G, z = {}G'.format(x / 9.806, y / 9.806, z / 9.806))

    # Plot sensor readouts as tuple on graph
    print((sensor.temperature, sensor.relative_humidity))
    # print((x, y, z))
    sleep(3)

