#project/auto/tissueRetraction/repos/Tests

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

DIR = 38    #Direction GPIO Pin
STEP = 40   #Step GPIO Pin
CW = 1      #Clockwise Rotation
CCW = 0     #Counterclockwise roation
SPR = 200   #Steps per Revolution (360/7.5)

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

step_count = 400
delay = 0.0075 # 1 second / SPR

cycles = 6
for x in range(cycles):
    GPIO.output(DIR, CCW)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    sleep(.5)
    GPIO.output(DIR, CW)

    for x in range(step_count - 100):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    sleep(.5)