import cv2

# initialize the camera
cam = cv2.VideoCapture(0)
ret, image = cam.read()

if ret:
    cv2.imwrite('SnapshotTest.jpg',image)
cam.release()