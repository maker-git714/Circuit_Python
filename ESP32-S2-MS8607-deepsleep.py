
# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_ms8607 import MS8607
import alarm
import time
import neopixel

i2c = board.I2C()
sensor = MS8607(i2c)
# Create instance of Neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

print("Pressure: %.2f hPa" % sensor.pressure)
print("Temperature: %.2f C" % sensor.temperature)
print("Humidity: %.2f %% rH" % sensor.relative_humidity)
print("\n------------------------------------------------\n")
print((sensor.relative_humidity, sensor.temperature))
pixel.fill((255, 0, 255))
time.sleep(0.1)


# Create a an alarm that will trigger 30 seconds from now.
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 30)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
