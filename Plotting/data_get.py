#project/auto/tissueRetraction/repos/Plotting

import csv
import random
import time
import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

x_value = 0
total_1 = -300000

fieldnames = ["x_value", "total_1"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file,  fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    reading = hx.get_raw_data_mean(readings=1)

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1
        }
        total_1 = reading
        csv_writer.writerow(info)
        print(x_value, total_1)

        x_value += 1
        total_1 = reading

    time.sleep(1)