import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as pyplot
from picamera2 import Picamera2

#functions
import HSV_filter as hsv
import shape_recognition as shape
import triangulation as tri
###import calibrarion as calib

#Open both cameras

cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap_left = cv2.VideoCapture(1, cv2.CAP_DSHOW)

frame_rate =120    #Camera frame rate

B = 9              #Distance between Cameras [cm]
f = 6              #Camera focal length [mm]
alpha = 56.6       #Camera field of view in the horizonal plane [degrees], How do I find this out and how does the affect the stereo sensing

count =-1

while(True):
    count += 1

    ret_right, frame_right = cap_right.read()  #Return determines if these frames can be opened
    ret_left, frame_left = cap_left.read()

############ CALIBRATION ################################

#frame_right , frame_left = calib.undistorted(frame_right, frame_left)

###################################################################
 # IF cannor catch any frame, break
    if ret_right==False or ret_left==False:
        print("NO IMAGES")
        break
    else:
        #apply HSV filter
        mask_right = hsv.add_HSV_filter(frame_right, 1)
        mask_left = hsv.add_HSV_filter(frame_left, 0)

        #result-frames after applying HSV filter mask
        res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        res_left = cv2.bitwise_and(frame_left, frame_left, mask=left)

        # Applying Shape recognition, WILL LIKELY CHNAGE FOR FIDUCIIAL RECOGNITION
        circles_right = shape.find_circles(frame_right, mask_right)
        circles_left = shape.find_circles(frame_left, mask_left)

        # Hough Transforms can be used as well or smae neural network to do object detection

        ####################### CALCULATING DEPTH #######################

    # If no ball can be caught in one camera show text 'TRACKING LOST'
    if np.all(circles_right) == None or np.all(circles_left) == None:
        cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    else:
        #Functions to calculate depth of object. Outputs vector of all depths in case of several balls.
        #All formulas used to find depth is in video presentation
        depth = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)

        cv2.putText(frame_right, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        cv2.putText(frame_left, "TRACKING", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        cv2.putText(frame_right, "Distance :" + str(round(depth,5)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        cv2.putText(frame_left, "Distance :" + str(round(depth,5)), (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)

        print("Depth: ", depth)


    #show the frames
    cv2.imshow("frame right", frame_right)
    cv2.imshow("frame left", frame_left)
    cv2.imshow("mask right", mask_right)
    cv2.imshow("mask left", mask_left)

    #Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Release and desroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()



