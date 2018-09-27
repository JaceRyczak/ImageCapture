import cv2 
import numpy as np 
import time
import os

#Variable Declaration
cap_enable = False 
img_counter = 0
delta_best = 5
arr_rgb = []
rgb_ok = False

#Threshold Settings
thrs_still = 3
thrs_move = 10

# define function for doing image difference calculation.
def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

#create and name some windows to display realtime images (for commissioning only)
winName = "Movement Indicator"
cv2.namedWindow(winName)
winName1 = "Actual Image"
cv2.namedWindow(winName1)

 
# select video feed device and set desired image size and frequency of feed.
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_CONTRAST, 0.15)
cam.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
print("FPS:", cam.get(cv2.CAP_PROP_FPS))
print("Width:", cam.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Brightness:", cam.get(cv2.CAP_PROP_BRIGHTNESS))
print("Contrast:", cam.get(cv2.CAP_PROP_CONTRAST))
print("AutoFocus:", cam.get(cv2.CAP_PROP_AUTOFOCUS))
print("Exposure:", cam.get(cv2.CAP_PROP_EXPOSURE))
ret, img_hold = cam.read() 					

# Read three initial images and convert to 1D
img1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

while True:
	start_total = time.time()	
	start = time.time()	
	

	# calculate differential image average pixel value	
	img_delta = np.average(diffImg(img1, img2, img3))		
	print("Delta is ", img_delta)	
	print("T1:", time.time()-start)
	
	
	# calculate average RGB values
	start = time.time()	
	img_rgb = np.array(img_hold)
	arr_rgb = np.mean(img_rgb, axis=(0,1))
	for x in arr_rgb:
		if x > 80:
			rgb_ok = True
	print("T2:", time.time()-start)


	cv2.imshow( winName, diffImg(img1, img2, img3) )
	start = time.time()
	cv2.imshow( winName1, img_hold)
	print("T3:", time.time()-start)


	#if average value of difference is less than threshold, enable capture
	start = time.time()	
	if img_delta < thrs_still:						
		cap_enable = True
	print("T4:", time.time()-start)


	# once enabled, compare newest image stillness with best historical image stillness and if better, save image for writing later.	
	start = time.time()	
	if cap_enable and img_delta < delta_best and rgb_ok:
			delta_best = img_delta
			img_best = img_hold
	print("T5:", time.time()-start)


	# once image has movement again, save the stillest image captured and reset flags for next time movement stops.
	start = time.time()
	if img_delta > thrs_move and cap_enable:
		img_counter += 1		
		img_name = "/home/marswodonga/code/ImageCapture/images/{}.jpg".format(delta_best)
		cv2.imwrite(img_name, img_best)
		cap_enable = False
		delta_best = thrs_move
	print("T6:", time.time()-start)

	
	# Read next images for next loop.
	start = time.time()	
	img1 = img2
	img2 = img3
	img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
	print("T7:", time.time()-start)
	start = time.time()	
	ret, img_hold = cam.read()
	rgb_ok = False
	k = cv2.waitKey(1)
	print("T8:", time.time()-start)


	#start = time.time()
	if k%256 == 27:
        	# ESC pressed
        	print("Escape hit, closing...")
        	break
	#print("T8:", time.time()-start)
	print("Run Time (s):", (time.time() - start_total))
cam.release()
cv2.destroyAllWindows()	 
print("Goodbye")


