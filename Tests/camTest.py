import cv2
import time
from picamera2 import Picamera2

picam2 = Picamera2(0)
picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)}, main={"format":'RGB888',"size": (640,480)}))
picam2.start()
time.sleep(2)

while True:
    img = picam2.capture_array()
    cv2.imshow("outpte", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
picam2.close