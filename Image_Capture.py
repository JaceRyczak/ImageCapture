import cv2  
import time
import numpy as np

#Variable Declaration
cap_enable = False 
img_counter = 0
delta_best = 5

#Threshold Settings
thrs_still = 2
thrs_move = 5

# define function for doing image difference calculation.
def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)
 
# select video feed device and set desired image size and frequency of feed.
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
cam.set(cv2.CAP_PROP_FPS, 30)
print("FPS:", cam.get(cv2.CAP_PROP_FPS))
ret, img_hold = cam.read() 					

# Read three initial images and convert to 1D
img1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:
	# calculate differential image average pixel value	
	img_delta = np.average(diffImg(img1, img2, img3))		
	#if average value of difference is less than threshold, enable capture	
	if img_delta < thrs_still:						
		cap_enable = True
	# once enabled, compare newest image stillness with best historical image stillness and if better, save image for writing later.	
	if cap_enable:
		if img_delta < delta_best:
			delta_best = img_delta
			img_best = img_hold
	# once image has movement again, save the stillest image captured and reset flags for next time movement stops.
	if img_delta > thrs_move and cap_enable:
		img_counter += 1		
		img_name = "test_image{}.png".format(img_counter)
		cv2.imwrite(img_name, img_best)
		cap_enable = False
		delta_best = thrs_move
	
	# Read next images for next loop.
	img1 = img2
	img2 = img3
	img3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
	ret, img_hold = cam.read()
	 
print("Goodbye")


