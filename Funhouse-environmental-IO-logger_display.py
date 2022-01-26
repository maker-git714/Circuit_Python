# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This example demonstrates how to log temperature on the FunHouse. Due to the sensors being near the
power supply, usage of peripherals generates extra heat. By turning off unused peripherals and back
on only during usage, it can lower the heat. Using deep sleep in between readings will also help.
By using an offset, we can improve the accuracy even more. Improving airflow near the FunHouse will
also help.
Adapted to display sensor data on the OLED with use of labels.
Putting ESP32-S2 microcontroller and display to Deep Sleep to minimize heat.
"""

from adafruit_funhouse import FunHouse
import alarm
import time
import microcontroller

funhouse = FunHouse(default_bg=0x000000, scale=3)

DELAY = 300
FEED_T = "temp"
FEED_H = "r-humid"
FEED_P = "atmo"
FEED_C = "cpu"
TEMPERATURE_OFFSET = (
    4  # Degrees C to adjust the temperature to compensate for board produced heat
)

# Turn things off
funhouse.peripherals.dotstars.fill(0)
funhouse.display.brightness = 0
funhouse.network.enabled = False

# create the labels
funhouse.display.show(None)  # speed up display by not refreshing until all sensors are loaded
#pir_label = funhouse.add_text(text="MOTION", text_position=(20, 10), text_color=0xFF0000)  # red text
temp_label = funhouse.add_text(text="TEMP:", text_position=(1, 10), text_color=0xE5F20C)
humid_label = funhouse.add_text(text="HUMID:", text_position=(1, 30), text_color=0xE5F20C)
pressure_label = funhouse.add_text(text="PRESSURE:", text_position=(1, 50), text_color=0xFF0000)
cpu_label = funhouse.add_text(text="CPU:", text_position=(1, 70), text_color=0x39AB07)



def log_data():
    print("Logging Temperature, Humidity and Pressure")
    print("Temperature %0.1F" % (funhouse.peripherals.temperature - TEMPERATURE_OFFSET))
    print("Humidity %0.0F %%" % (funhouse.peripherals.relative_humidity))
    print("Pressure %0.0F hPa" % (funhouse.peripherals.pressure))
    print("CPU_Temp %0.1F C" % (microcontroller.cpu.temperature))
    # Turn on WiFi
    funhouse.network.enabled = True
    # Connect to WiFi
    funhouse.network.connect()
    # Push to IO using REST
    funhouse.push_to_io(FEED_T, funhouse.peripherals.temperature - TEMPERATURE_OFFSET)
    funhouse.push_to_io(FEED_H, funhouse.peripherals.relative_humidity)
    funhouse.push_to_io(FEED_P, funhouse.peripherals.pressure)
    funhouse.push_to_io(FEED_C, microcontroller.cpu.temperature)
    # Turn off WiFi
    funhouse.network.enabled = False

funhouse.display.brightness = 0.3
funhouse.set_text("Temp:%0.1F C" % (funhouse.peripherals.temperature - TEMPERATURE_OFFSET), temp_label)
funhouse.set_text("Humid:%.0F %% rH" % funhouse.peripherals.relative_humidity, humid_label)
funhouse.set_text("Press:%.0F hPa" % funhouse.peripherals.pressure, pressure_label)
funhouse.set_text("CPU:%0.1F C" % microcontroller.cpu.temperature, cpu_label)

print(funhouse.peripherals.temperature, funhouse.peripherals.relative_humidity, funhouse.peripherals.pressure, microcontroller.cpu.temperature)
funhouse.display.show(funhouse.splash)
time.sleep(5)

log_data()
print("Sleeping for {} seconds...".format(DELAY))
    #funhouse.enter_light_sleep(DELAY)

# Create a an alarm that will trigger 30 seconds from now.
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + DELAY)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
