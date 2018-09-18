import cv2 
import time
import numpy as np

hysteresis = True 
img_counter = 0

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)
 
cam = cv2.VideoCapture(0)
 
winName = "Movement Indicator"
cv2.namedWindow(winName)
winName1 = "Actual Image"
cv2.namedWindow(winName1)
 
# Read three initial images
img1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
ret, img_hold = cam.read()

while True:
	img_counter += 1
	cv2.imshow( winName, diffImg(img1, img2, img3) )
	average = np.average(diffImg(img1, img2, img3))
	print("average is:", average)
	if average < 2 and hysteresis:
		img_name = "test_image{}.png".format(img_counter)
		cv2.imwrite(img_name, img_hold)
		hysteresis = False
	if average > 5:
		hysteresis = True
	# Read next image
	img1 = img2
	img2 = img3
	img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
	ret, img_hold = cam.read()
	cv2.imshow( winName1, img_hold)
	
	key = cv2.waitKey(10)
	if key == 27:
    		cv2.destroyWindow(winName)
    		break
 
print("Goodbye")
