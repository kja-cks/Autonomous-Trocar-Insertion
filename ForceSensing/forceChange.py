import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

hx.zero
input ('remove everything')
setZero = -(hx.get_data_mean(readings = 1))
input('Place known weight on scale')
cali = -(hx.get_data_mean(readings = 1))

weight = input('input weight')
value = float(weight)

ratio = value/(cali - setZero)
print(ratio)
print(setZero)
print(cali)

while True:
    poop = (-(hx.get_data_mean(readings = 50)) - setZero)*(ratio)
    print(poop)