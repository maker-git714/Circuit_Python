# SPDX-FileCopyrightText: 2020 by Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# modified to use AHT20 sensor to provide temperature and humidity data

import time
import board
import adafruit_ahtx0
import adafruit_sgp40

# Boards i2c bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sgp = adafruit_sgp40.SGP40(i2c)
aht = adafruit_ahtx0.AHTx0(i2c)


while True:
    temperature = aht.temperature
    humidity = aht.relative_humidity

    # For compensated raw gas readings
    """
    compensated_raw_gas = sgp.measure_raw(
        temperature=temperature, relative_humidity=humidity
    )
    print("Raw Data:", compensated_raw_gas)
    """

    # For Compensated voc index readings
    # The algorithm expects a 1 hertz sampling rate. Run "measure index" once per second.
    # It may take several minutes for the VOC index to start changing
    # as it calibrates the baseline readings.
    voc_index = sgp.measure_index(temperature=temperature, relative_humidity=humidity)

    print("VOC Index:", voc_index)
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.0f %% rH" % humidity)
    print("")
    time.sleep(1)
