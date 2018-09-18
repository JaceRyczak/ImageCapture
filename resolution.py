import cv2 
import time

cam = cv2.VideoCapture(0)
 
winName = "Movement Indicator"
cv2.namedWindow(winName)

print("width:", cv2.cv.CV_CAP_PROP_FRAME_WIDTH)

while True:
	time.sleep(0.5)
	ret, img_hold = cam.read()
	cv2.imshow( winName, img_hold)

	key = cv2.waitKey(10)
	if key == 27:
    		cv2.destroyWindow(winName)
    		break
