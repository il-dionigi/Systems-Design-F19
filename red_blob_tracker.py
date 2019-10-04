#Charles Zaloom

from __future__ import print_function
from collections import deque
import numpy as np
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import numpy as np
from skimage import io

buf = 32

#---------------
 
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=buf)
counter = 0
(dX, dY) = (0, 0)
direction = ""
 
camera = cv2.VideoCapture(0)

maskHSVL = np.array([0,0,100]);
maskHSVU = np.array([55,50,255]);

while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	FRAME = frame

	mask = cv2.inRange(frame, maskHSVL, maskHSVU)
	frame = cv2.bitwise_and(frame, frame, mask = mask)
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=1200)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	MASK = cv2.erode(hsv, None, iterations=2)
	MASK = cv2.dilate(MASK, None, iterations=2)

	hz, sz, MASK = cv2.split(MASK)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(MASK.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		cv2.putText(FRAME, "Center point: (" + str(center[0] - 640) + ", " + str((center[1] - 360) * -1) + ")", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(FRAME, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(FRAME, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
 
			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"
 
			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"
			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)
 
			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY
	# otherwise, compute the thickness of the line and
		# draw the connecting lines
			thickness = int(np.sqrt(buf / float(i + 1)) * 2.5)
			cv2.line(FRAME, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(FRAME, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(FRAME, "dx: {}, dy: {}".format(dX, dY),
		(10, FRAME.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.55, (0, 0, 255), 1)
 
	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", FRAME)
	key = cv2.waitKey(1) & 0xFF
	counter += 1
 
	# if the 'q' key is pressed, stop the loop
	if key == 27:#ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
