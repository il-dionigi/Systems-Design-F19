from __future__ import print_function
#from imutils.video import WebcamVideoStream
#from imutils.video import FPS
#import imutils
import cv2
import time 
import sys

vs = cv2.VideoCapture(0)
_, frame = vs.read()

scale_percent = 60 # percent of original size
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)
dim = (width, height)

while (1):
	_, frame = vs.read()
	#frame = imutils.resize(frame, width=400)
	frame = cv2.resize(frame, dim)
	
	#Press ESC key to kill
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
		
vs.release()

# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)
 
    # Display results
    cv2.imwrite("Results", im)

inputImage = frame

qrDecoder = cv2.QRCodeDetector()
 
# Detect and decode the qrcode
data,bbox,rectifiedImage = qrDecoder.detectAndDecode(inputImage)
if len(data)>0:
    print("Decoded Data : {}".format(data))
    display(inputImage, bbox)
    rectifiedImage = np.uint8(rectifiedImage);
    cv2.imwrite("Rectified QRCode", rectifiedImage);
else:
    print("QR Code not detected")
    cv2.imwrite("Results", inputImage)
 
cv2.waitKey(0)
cv2.destroyAllWindows()
