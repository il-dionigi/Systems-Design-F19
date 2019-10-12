import numpy as np
import cv2

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
ret,frame = cap.read() # return a single frame in variable `frame`

cv2.imwrite('test_image.png',frame)

cap.release()