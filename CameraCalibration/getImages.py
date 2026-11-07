import cv2
from picamera2 import Picamera2

picam1 = Picamera2(0)
picam1.configure(picam1.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam1.start()

num = 0

while (True):

    img = picam1.capture_array()

    k = cv2.waitKey(5)

    if k == ord("1"):
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('/home/kjacks/project/auto/tissueRetraction/repos/CameraCalibration/Calimages/caliImage' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()