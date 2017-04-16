
import cv2
import numpy as np
import time
import pylab
from numpy import linalg
from numpy.linalg import norm
import SetTrackBar as ST

#Windows
cv2.namedWindow("Original Image")
cv2.namedWindow('controller')
cv2.namedWindow('controller-2')
cv2.namedWindow('thresholded')
cv2.namedWindow('thresholded-2')
cv2.namedWindow("temp")
ST.SetTrackBarsBlue()

distance2Line = 0
lastdistance = 0
#Main Loop
def FindBlueObject(frame,hsv,listed):

	## Get Threshold Parameters
	## TODO: Get these parameters from calibration
	hl= cv2.getTrackbarPos('Hlow','controller-2')
	sl= cv2.getTrackbarPos('Slow','controller-2')
	vl= cv2.getTrackbarPos('Vlow','controller-2')
	hh= cv2.getTrackbarPos('Hhigh','controller-2')
	sh= cv2.getTrackbarPos('Shigh','controller-2')
	vh= cv2.getTrackbarPos('Vhigh','controller-2')

	## Get Morphological Operation Kernel Size
	ker_size=cv2.getTrackbarPos('Kernel Size','controller')
	ker_size2=cv2.getTrackbarPos('Kernel2 Size','controller')


	# Create the kernel 
	h=np.kaiser(ker_size,1)
	kernel=np.sqrt(np.outer(h,h))

	# Create the kernel 2
	h2=np.kaiser(ker_size2,1)
	kernel2=np.sqrt(np.outer(h2,h2))

	# Create the low and high boundaries
	low=np.array([hl,sl,vl], dtype=np.uint8) #Lower limits
	high=np.array([hh,sh,vh], dtype=np.uint8) #Upper limits

	# Threshold image
	thresh=cv2.inRange(hsv, low, high) #Thresholded image

	# Morphological Operations
	thresh=cv2.erode(thresh,kernel,iterations=2)
	thresh=cv2.dilate(thresh,kernel2,iterations=2)
	cv2.imshow("thresholded",thresh)


	# Detect Edges
	edges = cv2.Canny(thresh,50,200)
	contours,hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# Object Calculations starts here
	try:
		temp=frame.copy()
		temp2=frame.copy()

		count=0
		max_area=1000
		for cnt in contours:
			area=cv2.contourArea(cnt)
			if area>max_area:
				count = count + 1

		
		if (len(contours)>0)&(count>0):
			listed=sorted(contours, key=cv2.contourArea, reverse=True)
			cv2.fillConvexPoly(temp,listed[0],[255,0,0])
			temp=cv2.inRange(temp,np.array([250,0,0]),np.array([260,5,5]))
		else:
			temp=thresh.copy()
		
		rect = cv2.minAreaRect(listed[0])

		ellipse=cv2.fitEllipse(listed[0])

		# Take theta values from ellipse object
		theta_rad = np.deg2rad(ellipse[2])
		# Compose a unit vector for the line
		unitvec = [np.sin(theta_rad),-np.cos(theta_rad)]
		# Calculated the length of the line
		length = 0.3*np.sqrt(np.absolute(ellipse[1][0]*ellipse[1][0] - ellipse[1][1]*ellipse[1][1]))
		# Calculate the line points
		offset = np.multiply(unitvec,length)    

		# Calculate two points of line    
		point1_obj1 = ellipse[0] + offset
		point2_obj1 = ellipse[0] - offset
	
		# Draw the line
		A = cv2.line(frame,(int(point1_obj1[0]),int(point1_obj1[1])),(int(point2_obj1[0]),int(point2_obj1[1])),(255,255,0),2)
		
		return listed
	except:
		print("Object is not detected")
		return 0;
	#return listed
	#end = time.time()
