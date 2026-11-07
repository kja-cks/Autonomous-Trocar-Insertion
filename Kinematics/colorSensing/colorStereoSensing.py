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
###import calibrarion as cal

#Left Camera
picam1 = Picamera2(0)
picam1.configure(picam1.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam1.start()

#right camera
picam2 = Picamera2(1)
picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam2.start()

time.sleep(2)

#Open both cameras

cap_right = picam1
cap_left = picam2

frame_rate =120    #Camera frame rate

B = 2.8            #Distance between Cameras [cm]
f = 3.04              #Camera focal length [mm]
alpha = 62.2      #Camera field of view in the horizonal plane [degrees], How do I find this out and how does the affect the stereo sensing

count =-1

while(True):
    count += 1

    frame_right = picam1.capture_array()  #Return determines if these frames can be opened
    frame_left = picam2.capture_array()

############ CALIBRATION ################################

#frame_right , frame_left = calib.undistorted(frame_right, frame_left)

###################################################################
 # IF cannor catch any frame, break
    # if ret_right==False or ret_left==False:
    #     print("NO IMAGES")
    #     break
   # else:
        #apply HSV filter
    mask_right = hsv.add_HSV_filter(frame_right, 1)
    mask_left = hsv.add_HSV_filter(frame_left, 0)

    #result-frames after applying HSV filter mask
    res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
    res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left)

    # Applying Shape recognition, WILL LIKELY CHNAGE FOR FIDUCIIAL RECOGNITION
    circles_right = shape.find_circles(frame_right, mask_right)
    circles_left = shape.find_circles(frame_left, mask_left)

        # Hough Transforms can be used as well or smae neural network to do object detection

        ####################### CALCULATING DEPTH #######################

    # If no ball can be caught in one camera show text 'TRACKING LOST'
    if np.all(circles_right) == None or np.all(circles_left) == None:
        cv2.putText(frame_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,200), 2)
        cv2.putText(frame_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,200), 2)

    #else:
        #Functions to calculate depth of object. Outputs vector of all depths in case of several balls.
        #All formulas used to find depth is in video presentation
        #depth, xCoord, yCoord = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)

        #cv2.putText(frame_right, "TRACKING", (60,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
       # cv2.putText(frame_left, "TRACKING", (60,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
       # cv2.putText(frame_right, "Z Coordinate :" + str(round(depth,5)), (60,80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
       # cv2.putText(frame_left, "Z Coordinate :" + str(round(depth,5)), (60,80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        #cv2.putText(frame_right, "X Coordinate :" + str(round(xCoord,5)), (60,110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        #cv2.putText(frame_left, "X Coordinate :" + str(round(xCoord,5)), (60,110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        #cv2.putText(frame_right, "Y Coordinate :" + str(round(yCoord,5)), (60,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        #cv2.putText(frame_left, "Y Coordinate :" + str(round(yCoord,5)), (60,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)

        #print("Depth: ", depth)
        #print("Z Coordinate:" + str(depth,) + "  X Coordinate:" + str(xCoord) + "  Y Coordinate:" + str(yCoord))


    #show the frames
    cv2.imshow("frame right", frame_right)
    cv2.imshow("frame left", frame_left)
    cv2.imshow("mask right", mask_right)
    cv2.imshow("mask left", mask_left)

    #Hit "q" to close the window
    #print(circles_right)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Release and desroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()