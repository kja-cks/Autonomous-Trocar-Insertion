import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as pyplot
from picamera2 import Picamera2

import rtde_control
import rtde_receive

import URestimatorFunction as est
import URarucoTriangulation as tri

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

B = 3            #Distance between Cameras [cm]
f = 3.04              #Camera focal length [mm]
alpha = 62.2      #Camera field of view in the horizonal plane [degrees], How do I find this out and how does the affect the stereo sensing

#Outputs of Camera Calibration
camMatrix = np.array([[651.66411605, 0.0000000000, 316.64134348],
                      [0.0000000000, 651.69560803, 245.37397170],
                      [0.0000000000, 0.0000000000, 1.0000000000]])

newCameraMatrix = np.array([[640.75238309, 0.0000000000, 315.87038045],
                            [0.0000000000, 640.30742574, 245.41672910],
                            [0.0000000000, 0.0000000000, 1.0000000000]])

distMatrix = np.array([[ 3.17640421e-01, -1.18687997, -1.17158264e-03, -2.74307747e-04]])

count =-1

#################### ROBOT SETUP #######################

ROBOT_IP = "192.168.0.197"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

rtde_c.setTcp([337.128, 0, - 51, 0, 0, 0])

cv2.Rodrigues(rvec_left)
xPosTrans = 0
yPosTrans = 0
zPosTrans = 0

xRotTrans = 0
yRotTrans = 0
zRotTrans = 0


while(True):
    count += 1

    img_right = picam1.capture_array()
    img_left = picam2.capture_array()

    frame_right = cv2.undistort(img_right, camMatrix, distMatrix, None, newCameraMatrix)
    frame_left = cv2.undistort(img_left, camMatrix, distMatrix, None, newCameraMatrix)

    #frame_right = picam1.capture_array()
    #frame_left = picam2.capture_array()



    ###################### ARUCO DETECTION ########################

    centers_left, ids_left, detect_left, gray_left, corners_left, xCenter_left, yCenter_left, rvec_left = est.arucoDetection(img_left, camMatrix, distMatrix)
    centers_right, ids_right, detect_right, gray_right, corners_right, xCenter_right, yCenter_right, rvec_right = est.arucoDetection(img_right, camMatrix, distMatrix)

    ####################### CALCULATING DEPTH #######################

    # If no marker can be caught in one camera show text 'TRACKING LOST'
    if len(corners_right) == 0 or len(corners_left) == 0:
        cv2.putText(detect_right, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,200), 2)
        cv2.putText(detect_left, "TRACKING LOST", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,200), 2)

    else:
        #Functions to calculate depth of object. Outputs vector of all depths in case of several balls.
        #All formulas used to find depth is in video presentation


        depth, xCoord, yCoord = tri.find_depth(xCenter_right, yCenter_right, xCenter_left, yCenter_left, img_right, img_left, B, f, alpha, corners_right)
        xrot_left, yrot_left, zrot_left = rvec_left #Getting individual components of rotation vectors
        xrot_right, yrot_right, zrot_right = rvec_right

        #Translating stero sensor data from millimeters to meters
        xPos = xCoord *0.001
        yPos = yCoord *0.001
        zPos = depth *0.001

        target_pose = [xPos + xPosTrans, yPos + yPosTrans, zPos + zPosTrans, xrot_left + xRotTrans, yrot_left + yRotTrans, zrot_left + zRotTrans]
        rtde_c.moveL(target_pose, speed=0.3, acceleration=0.5)

        cv2.putText(detect_right, "TRACKING", (40,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 1)
        cv2.putText(detect_left, "TRACKING", (40,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 1)
        cv2.putText(detect_right, "Z Coordinate :" + str(round(depth,5)), (50,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "Z Coordinate :" + str(round(depth,5)), (50,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_right, "X Coordinate :" + str(round(xCoord,5)), (50,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "X Coordinate :" + str(round(xCoord,5)), (50,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_right, "Y Coordinate :" + str(round(yCoord,5)), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "Y Coordinate :" + str(round(yCoord,5)), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_right, "Z Rotation :" + str(zrot_right), (50,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "Z Rotation :" + str(zrot_left), (50,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_right, "X Rotation :" + str(xrot_right), (50,140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "X Rotation :" + str(xrot_left), (50,140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_right, "Y Rotation :" + str(yrot_right), (50,160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)
        cv2.putText(detect_left, "Y Rotation :" + str(yrot_left), (50,160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (124,252,0), 1)


        ################ Draw Center Point ####################
        cv2.circle(detect_right, (int(xCenter_right), int(yCenter_right)), 3, (0,255,255), -1)
        cv2.circle(detect_left, (int(xCenter_left), int(yCenter_left)), 3, (0,255,255), -1)
        #print("Depth: ", depth)
        #print("Z Coordinate:" + str(depth,) + "  X Coordinate:" + str(xCoord) + "  Y Coordinate:" + str(yCoord))


    #show the frames
    cv2.imshow("frame right", img_right)
    cv2.imshow("frame left", img_left)
    cv2.imshow("detect right", detect_right)
    cv2.imshow("detect left", detect_left)
    print(rvec_left)

    #Hit "q" to close the window
    #print(circles_right)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Release and desroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()