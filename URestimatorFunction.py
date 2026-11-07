import cv2
import numpy as np
import sys
import time
from picamera2 import Picamera2

def arucoDetection(frame, camMatrix, distMatrix):

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11,
    }

    #Defining Detection Parameters
    aruco_type = "DICT_4X4_50"
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    #Creating Center Points
    testPoints = ([(0, 0, 0),
                   (0, 5, 0),
                   (5, 5, 0),
                   (5, 0, 0),
                   (2.5, 2.5, 0),
                   (0, 0, 0)])
    objectPoints = np.array(testPoints, dtype=np.float32)

    #Adding Centers to Corner Arrays
    centers = []

    x_avg = 0

    y_avg = 0

    rvec =[]

    allPoints = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    med = []

    cornCentersWithZeros = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    cornCenters = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                   None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)
    image_with_markers = frame.copy()

    k = cv2.waitKey(5)

    #Drawing Detections
    if len(corners) > 0:

        for i in range(0, len(ids)):

            points = corners[i]
            flatten = points.flatten()

            ##### Defining X and Y coordinates of Centers ################
            x_cords = flatten[::2]
            x_avg = np.mean(x_cords, axis = 0)
            y_cords = flatten[1::2]
            y_avg = np.mean(y_cords, axis = 0)

            center = np.mean(points, axis = 1)
            centers = np.append(med, center)
            cornCenters[i] = np.append(flatten, centers)

            addZeros = flatten[0:2] + np.array([0.000000000000000001, 0.00000000000000001])

            cornCentersWithZeros[i] = np.append(cornCenters[i], addZeros)
            allPoints[i] = np.reshape(cornCentersWithZeros[i], (6, 2))
            cv2.aruco.drawDetectedMarkers(gray, corners, ids)

            #Drawing Detections
            success, rvec, tvec = cv2.solvePnP(objectPoints, allPoints[i], camMatrix, distMatrix) #UPDATE IMAGE AND OBJECT POINTS
            cv2.drawFrameAxes(image_with_markers, camMatrix, distMatrix, rvec, tvec, 5, 2) #Figure out last Parameters
            cv2.aruco.drawDetectedMarkers(image_with_markers, corners, ids)
            print(x_avg)

    return centers, ids, image_with_markers, gray, corners, x_avg, y_avg, rvec


#picam1 = Picamera2(0)
#picam1.configure(picam1.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
#picam1.start()

#camMatrix = np.array([[3926.71816, 0.00000000, 955.011915],
#                     [0.00000000, 8852.07704, 610.351488],
#                      [0.00000000, 0.00000000, 1.00000000]])
#distMatrix = np.array([[-1.69551442e+00,  2.46187694e+01, -1.17677463e-02, -1.05421293e-01, -2.27019367e+02]])

#while True:
#   grame = picam1.capture_array()
#    centers_left, ids_left, detect_left, gray_left, corners_left, x_avg, y_avg = arucoDetection(grame, camMatrix, distMatrix)
#    cv2.imshow('detect left', detect_left)
#    if len(corners_left) == 0:
#        print('nothing')
#    else:
#        for i in range (0, len(ids_left)):
#            print(x_avg)
#            print(centers_left[i])