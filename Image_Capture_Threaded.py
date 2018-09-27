from __future__ import print_function
import cv2 
import numpy as np 
import datetime
import time
import os
import imutils
from threading import Thread
from queue import Queue
import argparse

class WebcamVideoStream:
	def __init__(self, src=1):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

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
cam = WebcamVideoStream(src=1).start()
cv2.VideoCapture(1).set(cv2.CAP_PROP_CONTRAST, 0.15)
cv2.VideoCapture(1).set(cv2.CAP_PROP_BRIGHTNESS, 0.6)
cv2.VideoCapture(1).set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cv2.VideoCapture(1).set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.VideoCapture(1).set(cv2.CAP_PROP_FPS, 30)
cv2.VideoCapture(1).set(cv2.CAP_PROP_AUTOFOCUS, 0)
print("FPS:", cv2.VideoCapture(1).get(cv2.CAP_PROP_FPS))
print("Width:", cv2.VideoCapture(1).get(cv2.CAP_PROP_FRAME_WIDTH))
print("Height:", cv2.VideoCapture(1).get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Brightness:", cv2.VideoCapture(1).get(cv2.CAP_PROP_BRIGHTNESS))
print("Contrast:", cv2.VideoCapture(1).get(cv2.CAP_PROP_CONTRAST))
print("AutoFocus:", cv2.VideoCapture(1).get(cv2.CAP_PROP_AUTOFOCUS))
print("Exposure:", cv2.VideoCapture(1).get(cv2.CAP_PROP_EXPOSURE))
img_hold = cam.read() 					

# Read three initial images and convert to 1D
img1 = cv2.cvtColor(cam.read(), cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(cam.read(), cv2.COLOR_BGR2GRAY)
img3 = cv2.cvtColor(cam.read(), cv2.COLOR_BGR2GRAY)

while True:
	start_total = time.time()	
	
	# calculate differential image average pixel value	
	img_delta = np.average(diffImg(img1, img2, img3))		
	print("Delta is ", img_delta)	
		
	# calculate average RGB values
	img_rgb = np.array(img_hold)
	arr_rgb = np.mean(img_rgb, axis=(0,1))
	for x in arr_rgb:
		if x > 80:
			rgb_ok = True
	
	cv2.imshow( winName, diffImg(img1, img2, img3) )
	cv2.imshow( winName1, img_hold)
	
	#if average value of difference is less than threshold, enable capture	
	if img_delta < thrs_still:						
		cap_enable = True
	# once enabled, compare newest image stillness with best historical image stillness and if better, save image for writing later.	
	if cap_enable and img_delta < delta_best and rgb_ok:
			delta_best = img_delta
			img_best = img_hold
	
	# once image has movement again, save the stillest image captured and reset flags for next time movement stops.
	if img_delta > thrs_move and cap_enable:
		img_counter += 1		
		img_name = "/home/marswodonga/code/ImageCapture/images/{}.jpg".format(delta_best)
		cv2.imwrite(img_name, img_best)
		cap_enable = False
		delta_best = thrs_move
	
	# Read next images for next loop.
	img1 = img2
	img2 = img3
	start = time.time()
	img3 = cv2.cvtColor(cam.read(), cv2.COLOR_BGR2GRAY)
	print("T7:", time.time()-start)
	start = time.time()	
	img_hold = cam.read()
	rgb_ok = False
	k = cv2.waitKey(1)
	print("T8:", time.time()-start)


	start = time.time()
	if k%256 == 27:
        	# ESC pressed
        	print("Escape hit, closing...")
        	break
	print("T8:", time.time()-start)
	print("Run Time (s):", (time.time() - start_total))

cam.stop()
cv2.destroyAllWindows()	 
print("Goodbye")


