import cv2
import time
from picamera2 import Picamera2

#Left Camera
picam1 = Picamera2(1)
picam1.configure(picam1.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam1.start()

#right camera
#picam2 = Picamera2(1)
#picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
#picam2.start()

time.sleep(2)

while (True):
    img1 = picam1.capture_array()

    #img2 = picam2.capture_array()

    cv2.imshow("outpte 1", img1)
    #cv2.imshow("outpte 2", img2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
picam2.close