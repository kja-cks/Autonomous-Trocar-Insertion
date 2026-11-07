import RPi.GPIO as GPIO
from hx711 import HX711
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Code Setup
plt.style.use('fivethirtyeight')

GPIO.setmode(GPIO.BCM)

hx = HX711(dout_pin=6, pd_sck_pin=5)

#Calibration
hx.zero
input ('remove everything')
setZero = (hx.get_data_mean(readings = 50))

startTime = time.time()
xTime = []
runTime = 0
forceReadings = []
duration = 20
endTime = startTime + duration
i = 0
velocity = [0]
adjusted = []
dilf=[]

#Taking Readings
while time.time() < endTime:
    reading = ((hx.get_raw_data_mean(readings = 1) - setZero)) * (0.0000107)
    if   -6 < reading < 50:
        forceReadings.append(reading)
        print(reading)
        xTime.append(runTime)
        time.sleep(0.1)
        i = i + 1
        runTime = i * 0.1
        if i > 1:
            dif = forceReadings[i-1] - forceReadings[i-2]
            dilf.append(dif)
            #print(abs(dif))
            if abs(dif) < 1:
                velocity.append(dif)
            else:
                velocity.append(0)
        adj = forceReadings[i-1] - sum(velocity)
        adjusted.append(adj)


print(forceReadings)
print(velocity)
print(adjusted)
print(dilf)
#print(ratio)
plt.figure()
plt.plot(xTime, forceReadings)
plt.title("Raw Readings")

plt.figure()
plt.plot(xTime, velocity)
plt.title("velocity")

plt.figure()
plt.plot(xTime, adjusted)
plt.title("Adjusted Readings")
plt.show()

plt.figure()
plt.plot(xTime, velocity)
plt.title("velocity")