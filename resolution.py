import cv2 
import time

cam = cv2.VideoCapture(0)
 
#winName = "Movement Indicator"
#cv2.namedWindow(winName)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam.set(cv2.CAP_PROP_FPS, 30)
#cam.set(cv2.CAP_PROP_CONVERT_RGB, False)
print("Width:", cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS:", cam.get(cv2.CAP_PROP_FPS))
while True:
	#time.sleep(0.5)
	ret, img_hold = cam.read()
	#cv2.imshow( winName, img_hold)

	#key = cv2.waitKey(10)
	#if key == 27:
    	#	cv2.destroyWindow(winName)
    	#	break

#create and name some windows to display realtime images (for commissioning only)
#winName = "Movement Indicator"
#cv2.namedWindow(winName)
#winName1 = "Actual Image"
#cv2.namedWindow(winName1)

#	cv2.imshow( winName, diffImg(img1, img2, img3) )
#	cv2.imshow( winName1, img_hold)	
#	img_delta = np.average(diffImg(img1, img2, img3))
#	print("Image stillness is:", img_delta)
#	print("cap_enable = ", cap_enable)
#	print("delta best = ", delta_best)
