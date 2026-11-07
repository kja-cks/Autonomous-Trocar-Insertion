import cv2
import numpy as np
import sys
import time
from picamera2 import Picamera2

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

#Matrices
camMatrix = np.array([[3.23556050e+03, 0.00000000e+00, 3.30424683e+02],
                      [0.00000000e+00, 3.11614610e+03, 2.42113289e+02],
                      [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distMatrix = np.array([[ 5.77025518e+00, -4.53888418e+02,  2.23863590e-02,  2.08368175e-03,
  -8.88903259e-01]])

#Defining Detection Parameters
aruco_type = "DICT_4X4_50"
aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

#left camera
picam1 = Picamera2(0)
picam1.configure(picam1.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam1.start()

#right camera
picam2 = Picamera2(1)
picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam2.start()

time.sleep(2)

cap_right = picam1
cap_left = picam2

detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
#image = cv2.imread("/home/kjacks/project/env/repos/AruCoMarkers/distort.png")
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#corners, ids, rejected = detector.detectMarkers(gray)

#Creating Center Points
#image_with_markers = image.copy()



testPoints = ([(0, 0, 0),
               (0, 5, 0),
               (5, 5, 0),
               (5, 0, 0),
               (2.5, 2.5, 0),
               (0, 0, 0)])
objectPoints = np.array(testPoints, dtype=np.float32)

#Adding Centers to Corner Arrays
centers = []
allPoints = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

med = []

#center = []

cornCentersWithZeros = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

cornCenters = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
               None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
               None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

#Drawing Detections
#points = corners[0]
#flatten = points.flatten()
#center = np.mean(points, axis = 1)
#centers = np.append(med, center)
#cornCenters[0] = np.append(flatten, centers)

#addZeros = flatten[0:2] + np.array([0.00000001, 0.0000001])

#cornCentersWithZeros[0] = np.append(cornCenters[0], addZeros)
#allPoints[0] = np.reshape(cornCentersWithZeros[0], (6, 2))
#cv2.aruco.drawDetectedMarkers(gray, corners, ids)
#Drawing Detections
#success, rvec, tvec = cv2.solvePnP(objectPoints, allPoints[0], camMatrix, distMatrix) #UPDATE IMAGE AND OBJECT POINTS
#cv2.drawFrameAxes(image_with_markers, camMatrix, distMatrix, rvec, tvec, 2, 5) #Figure out last Parameters

while (True):
    img = cap_right.capture_array()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)
    image_with_markers = img.copy()

    k = cv2.waitKey(5)

    if k == ord("1"):
        break

    #Drawing Detections
    if len(corners) > 0:

        for i in range(0, len(ids)):

            points = corners[i]
            flatten = points.flatten()

            x_cords = flatten[::2]
            x_avg = np.mean(x_cords, axis = 0)
            y_cords = flatten[1::2]
            y_avg = np.mean(y_cords, axis = 0)


            center = np.mean(points, axis = 1)
            centers = np.append(med, center)
            cornCenters[i] = np.append(flatten, centers)

            addZeros = flatten[0:2] + np.array([0.00000000000001, 0.0000000000001])

            cornCentersWithZeros[i] = np.append(cornCenters[i], addZeros)
            allPoints[i] = np.reshape(cornCentersWithZeros[i], (6, 2))
            cv2.aruco.drawDetectedMarkers(gray, corners, ids)

            #Drawing Detections
            success, rvec, tvec = cv2.solvePnP(objectPoints, allPoints[i], camMatrix, distMatrix) #UPDATE IMAGE AND OBJECT POINTS
            cv2.drawFrameAxes(image_with_markers, camMatrix, distMatrix, rvec, tvec, 5, 2) #Figure out last Parameters
            cv2.aruco.drawDetectedMarkers(image_with_markers, corners, ids)
            #print(x_cords)
            print(x_avg)
            #print(center[0[0]])

    cv2.imshow('Vid', img)
    cv2.imshow('Detection', image_with_markers)
    cv2.imshow('gray', gray)


cv2.imshow('detection', image_with_markers)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()