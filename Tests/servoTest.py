from gpiozero import AngularServo
import time

servo1 = AngularServo (17, min_pulse_width=0.0006, max_pulse_width = 0.0022)
servo2 = AngularServo (27, min_pulse_width=0.0006, max_pulse_width = 0.0022)

def servoOpen():
    servo1.angle = 90
    servo2.angle = -90

def servoClose():
    servo1.angle = -90
    servo2.angle = 90

servoOpen()

input("close")

servoClose()