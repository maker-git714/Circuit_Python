# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# using Featherwing HX8357 3.5" TFT with Feather M4
# output using MS8607 sensor data Temperature, Humidity, Pressure sensor

"""
This will initialize the display using displayio and draw a solid blue
background, a smaller black rectangle with border, and output sensor MS8607 
data with labeled text.
"""
from time import sleep
import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hx8357 import HX8357
from adafruit_ms8607 import MS8607

i2c = board.I2C()
sensor = MS8607(i2c)
temp = sensor.temperature
humidity = sensor.relative_humidity
pressure = sensor.pressure

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = HX8357(display_bus, width=480, height=320)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(480, 320, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x005c5c # blue background

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(460, 300, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000 # Black inner rectangle
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=10, y=10)
splash.append(inner_sprite)


# Draw a label by defining text group
text_group = displayio.Group(scale=3)
splash.append(text_group)


while True:
    # Define text labels with data
    text1 = "Temperature: %.1f C" % sensor.temperature
    text2 = "Humidity: %.1f %% rH" % sensor.relative_humidity
    text3 = "Pressure: %.1f hPa" % sensor.pressure

    # Create labels with font and color
    text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFFFF00, x=20, y=20) 
    text_group.append(text_area1)
    text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFA97E, x=20, y=50)
    text_group.append(text_area2)
    text_area3 = label.Label(terminalio.FONT, text=text3, color=0xA8B6AF, x=20, y=80)
    text_group.append(text_area3)

    sleep(10)

    # Clear screen to refresh labels
    text_group.remove(text_area1)
    text_group.remove(text_area2)
    text_group.remove(text_area3)
