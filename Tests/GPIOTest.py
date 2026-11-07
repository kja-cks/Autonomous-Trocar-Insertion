from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
DIR = 38    #Direction GPIO Pin
STEP = 40   #Step GPIO Pin
x=0

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

while x < 50:
    GPIO.output(STEP, GPIO.HIGH)
    sleep(1)
    GPIO.output(STEP, GPIO.LOW)
    sleep(1)
    x = x+1