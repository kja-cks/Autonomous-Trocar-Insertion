import RPi.GPIO as GPIO
from hx711 import HX711
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import sleep

GPIO.setmode(GPIO.BCM)

plt.style.use('fivethirtyeight')

hx = HX711(dout_pin=6, pd_sck_pin=5)

#Calibration
hx.zero
input ('remove everything')
setZero = (hx.get_data_mean(readings = 50))

startTime = time.time()
xTime = []
runTime = 0
forceReadings = []
duration = 50
endTime = startTime + duration
i = 0
velocity = [0]
adjusted = []
dilf=[]
peaktrack = 0

DIR = 20    #Direction GPIO Pin
STEP = 21   #Step GPIO Pin
CW = 1      #Clockwise Rotation
CCW = 0     #Counterclockwise roation
SPR = 200   #Steps per Revolution (360/7.5)

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

step_count = 400
delay = 0.0075 # 1 second / SPR

cycles = 6

while True:
    reading = ((hx.get_raw_data_mean(readings = 1) - setZero)) * (0.0000107)
    if   -6 < reading < 50:
        forceReadings.append(reading)
        #print(reading)
        xTime.append(runTime)
        i = i + 1
        runTime = i * 0.1
        if i > 1:
            dif = forceReadings[i-1] - forceReadings[i-2]
            #print (dif)
            dilf.append(dif)
            #print(abs(dif))
            if abs(dif) < 1:
                velocity.append(dif)
                if  dif > -0.75:
                    if peaktrack <= 1:
                        print(peaktrack)
                        print("poop")
                        GPIO.output(DIR, CCW)
                        GPIO.output(STEP, GPIO.HIGH)
                        sleep(delay)
                        GPIO.output(STEP, GPIO.LOW)
                elif -2< dif < -0.1:
                    print(dif)
                    print("balls")
                    peaktrack = peaktrack + 1
            else:
                velocity.append(0)
                print(peaktrack)

        adj = forceReadings[i-1] - sum(velocity)
        adjusted.append(adj)