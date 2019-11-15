from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
from pyzbar import pyzbar
import cv2
 
vs = WebcamVideoStream(src=0).start()

while (1):
	frame = vs.read()
	frame = imutils.resize(frame, width=800)

	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
	for barcode in barcodes:
		# extract the bounding box location of the barcode and draw the
		# bounding box surrounding the barcode on the frame
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	 
		# the barcode data is a bytes object so if we want to draw it on
		# our output frame we need to convert it to a string first
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
	 
		# draw the barcode data and barcode type on the frame
		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 0, 255), 2)
	 
		# print the barcode type and data to the terminal
		print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

	#Press ESC key to kill
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

	cv2.imshow("frame", frame)
 
# show the output frame
vs.stop()
cv2.waitKey(0)