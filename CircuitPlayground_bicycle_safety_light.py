# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example uses the accelerometer on the Circuit Playground.

https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration

Adapted to use accelerometer to sense deceleration of moving object i.e bicycle
Intensity of flashing is dependent on rate of deceleration of the x-axis and z-axis.
The accelerometer is oriented with x pointing to the sky-to enable lights to be visible.
"""
import time
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.05 # adjust LED brightness

def y_change():
    return int(1000*last_y - y)  # increase resolution for comparator to offset noise

def z_change():
    return int(1000*last_z -z)

last_y = 0.0
last_z = 0.0



while True:
    x, y, z = cp.acceleration
    #print((x, y, z))
    #print(z_change(), y_change())

    time.sleep(0.25)

    print(f"change in z axis = {z_change()}")
    print(f"change in y axis = {y_change()}")

    if   z_change() > 3000 or y_change() > -5000:  #compares change in z and y axis
        cp.pixels[0] = (255, 0, 0)
        cp.pixels[1] = (255, 0, 0)
        cp.pixels[2] = (255, 0, 0)
        cp.pixels[3] = (255, 0, 0)
        cp.pixels[4] = (255, 0, 0)
        cp.pixels[5] = (255, 0, 0)
        cp.pixels[6] = (255, 0, 0)
        cp.pixels[7] = (255, 0, 0)
        cp.pixels[8] = (255, 0, 0)
        cp.pixels[9] = (255, 0, 0)

        last_y = y
        last_z = z
        cp.pixels.show()
        time.sleep(0.3)
    else:
        cp.pixels[0] = (255, 140, 0)
        cp.pixels[2] = (255, 255, 255)
        cp.pixels[4] = (255, 140, 0)
        cp.pixels[5] = (255, 140, 0)
        cp.pixels[7] = (255, 255, 255)
        cp.pixels[9] = (255, 140, 0)

        last_y = y
        last_z = z
        cp.pixels.show()
        time.sleep(0.3)



    cp.pixels[0] = (0,0,0)
    cp.pixels[1] = (0,0,0)
    cp.pixels[2] = (0,0,0)
    cp.pixels[3] = (0,0,0)
    cp.pixels[4] = (0,0,0)
    cp.pixels[5] = (0,0,0)
    cp.pixels[6] = (0,0,0)
    cp.pixels[7] = (0,0,0)
    cp.pixels[8] = (0,0,0)
    cp.pixels[9] = (0,0,0)
    cp.pixels.show()

