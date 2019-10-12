import cv2

# initialize the camera
cam = cv2.VideoCapture(0)
ret, image = cam.read()


cv2.imwrite('SnapshotTest.jpg',image)
cam.release()
