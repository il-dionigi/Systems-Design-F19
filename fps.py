# Charles Zaloom

# This file shows 2 methods of vastly improving FPS of webcam video
# Method 1: Decreasing pixel count by scaling down image
# Method 2: Using the imutils library to put the webcam on a seperate thread

from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2

vs = WebcamVideoStream(src=0).start()

while (1):
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	cv2.imshow("Frame", frame)

	#Press ESC key to kill
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cv2.destroyAllWindows()
vs.stop()