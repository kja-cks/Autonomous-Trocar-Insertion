import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

x = 0

hx.zero
input ('remove everything')
setZero = (hx.get_data_mean(readings = 100))
#input('Place known weight on scale')
#cali = (hx.get_data_mean(readings = 100))

#weight = input('input weight')
#value = float(weight)

#print(setZero)
#print(cali)

#ratio = value/(cali - setZero)
#print(ratio)
print(setZero)
#print(cali)

while x <1000:
    poop = ((hx.get_data_mean(readings = 1)) - setZero)*(0.00107)
    print(poop)

    x=x+1

#print(ratio)
print(setZero)
#print(cali)