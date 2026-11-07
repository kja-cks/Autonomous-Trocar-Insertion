import sys
import cv2
import numpy as np
import time


def find_depth(circle_right, circle_left, frame_right, frame_left, baseline, f, alpha):

    # CONVERT FOCAL LENGTH f from [mm] TO [pixel]
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_right == width_left:
        #f_pixel = (width_right) / np.tan(alpha * 0.5 * np.pi/180)
        f_pixel = (f * width_right)/3.68  # (Focal length [mm] * Image width [pixels]) / Image Sensor width [mm]

    else:
        print('Left and right cmarera frame do not have the same width')

    x_right = circle_right[0] - (width_right/2)
    x_left = circle_left[0] - (width_right/2)
    y_right = circle_right[1] - (height_right/2)
    y_left = circle_left[1] - (height_left/2)


    # Calculate the disparity:
    disparity = x_left - x_right  #Displacemnent between left nd right frames [pixels]

    # Calculate Depth z:
    zDepth = (baseline*f_pixel)/disparity   #depth in [cm]
    xCoord = (x_left*zDepth)/f_pixel
    yCoord = (y_left*zDepth)/f_pixel

    return abs(zDepth), xCoord, yCoord