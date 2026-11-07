
################### WILL LIKELY CHANGE FOR FIDUCIAL RECOGNITION AND POSE ESTIMATION ############################

import sys
import cv2
import numpy as np
import time


def add_HSV_filter(frame, camera):

    #Blurring the frame
    blur = cv2.GaussianBlur(frame,(5,5), 0)

    #converting RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    l_b_r = np.array([0, 0, 50])
    u_b_r = np.array([30, 30, 255])
    l_b_l = np.array([0, 0, 60])
    u_b_l = np.array([30, 30, 255])

    if(camera == 1):
        mask = cv2.inRange(blur, l_b_r, u_b_r)
    else:
        mask = cv2.inRange(blur, l_b_l, u_b_l)

    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)

    return mask