# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT

# This is the stable version of ms8607-SSD1306 script
"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""
from time import sleep
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_ms8607 import MS8607

displayio.release_displays()

oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D, reset=oled_reset)
sensor = MS8607(i2c)

WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White



bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

while True:

    print("Pressure: %.2f hPa" % sensor.pressure)
    text3 = ("Pressure:%.2f hPa" % sensor.pressure)
    print("Temperature: %.2f C" % sensor.temperature)
    text1 = ("Temperature:%.2f C" % sensor.temperature)
    print("Humidity:%.2f %% rH" % sensor.relative_humidity)
    text2 = ("Humidity:%.2f %% rH" % sensor.relative_humidity)
    print("\n------------------------------------------------\n")

    # Draw a label
    #text1 = "TEMP- " + str(sensor.temperature) + " *C"
    #text2 = "HUMID-" + str(sensor.relative_humidity) + " %rH"
    #text3 = "PRESSURE-" + str(sensor.pressure) + " kPa"
    text_area1 = label.Label(
        terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=HEIGHT // 3 - 1
    )
    splash.append(text_area1)
    text_area2 = label.Label(
        terminalio.FONT, text=text2, color=0xFFFFFF, x=8, y=HEIGHT // 2 - 1
    )
    splash.append(text_area2)
    text_area3 = label.Label(
        terminalio.FONT, text=text3, color=0xFFFFFF, x=8, y=HEIGHT // 2 + 10
    )
    splash.append(text_area3)

    sleep(10)
    splash.remove(text_area1)   #
    splash.remove(text_area2)
    splash.remove(text_area3)

