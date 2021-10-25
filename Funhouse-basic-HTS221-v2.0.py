# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This example demonstrates how to log temperature on the FunHouse. Due to the sensors being near the
power supply, usage of peripherals generates extra heat. By turning off unused peripherals and back
on only during usage, it can lower the heat. Using light sleep in between readings will also help.
By using an offset, we can improve the accuracy even more. Improving airflow near the FunHouse will
also help.----Modified to use the HTS221 sensor to reading temperature
"""

from adafruit_funhouse import FunHouse
import time
import board
import adafruit_hts221
import microcontroller
from digitalio import DigitalInOut, Direction, Pull

funhouse = FunHouse(default_bg=0x000000, scale=3) #changes the size of the label
#funhouse = FunHouse(default_bg=None)

funhouse.peripherals.set_dotstars(0x800000, 0x808000, 0x008000, 0x000080, 0x800080) # rainbow colors

i2c = board.I2C()
hts = adafruit_hts221.HTS221(i2c)  #using hts to not conflict with sensor

# sensor setup
sensors = []
for p in (board.A0, board.A1, board.A2):
    sensor = DigitalInOut(p)
    sensor.direction = Direction.INPUT
    sensor.pull = Pull.DOWN
    sensors.append(sensor)

def set_label_color(conditional, index, on_color):
    """sets color of specific label index to an on or off color depending on condition"""
    if conditional:
        funhouse.set_text_color(on_color, index)  # when condition true on_color
    else:
        funhouse.set_text_color(0x057CE9, index)  # when false, label is colored blue


# create the labels
funhouse.display.show(None)  # speed up display by not refreshing until all sensors are loaded
pir_label = funhouse.add_text(text="MOTION", text_position=(20, 10), text_color=0xFF0000)  # red text
temp_label = funhouse.add_text(text="TEMP:", text_position=(1, 30), text_color=0x606060)
humid_label = funhouse.add_text(text="HUMID:", text_position=(1, 50), text_color=0x606060)
cpu_label = funhouse.add_text(text="CPU:", text_position=(1,70), text_color=0x606060)
funhouse.display.show(funhouse.splash)

#DELAY = 60

# Turn things off
funhouse.peripherals.dotstars.fill(5)
funhouse.display.brightness = 0.5
funhouse.network.enabled = False



while True:
    set_label_color(funhouse.peripherals.pir_sensor, pir_label, 0xFF0000) # red text if motion detected
    print("Temperature: %.1f C" % hts.temperature)
    set_label_color(hts, temp_label, 0xE5F20C) # yellow text
    funhouse.set_text("Temp:%0.1F C" % hts.temperature, temp_label)
    #time.sleep(3)
    print("Relative Humidity: %.0f%% rH" % hts.relative_humidity)
    set_label_color(hts, humid_label, 0xE5F20C) # yellow text
    funhouse.set_text("Humid:%.0F %% rH" % hts.relative_humidity, humid_label)
    #time.sleep(3)
    print("CPU Temperature: %.1f C" % microcontroller.cpu.temperature)
    set_label_color(hts, cpu_label, 0x39AB07) # green text
    funhouse.set_text("CPU:%.1F C" % microcontroller.cpu.temperature, cpu_label)
    #time.sleep(30)
    print("")
    
    #time.sleep(3)
    #funhouse.enter_light_sleep(DELAY)
