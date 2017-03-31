import ThreadedWebcam as CamLib

import cv2
import numpy as np
import time
import pylab
from numpy import linalg
from numpy.linalg import norm
import SetTrackBar as ST
 
## Multithread camera is finished here.


iLastX=-1
iLastY=-1

#Windows
cv2.namedWindow("Original Image")
cv2.namedWindow('controller')
cv2.namedWindow('controller-2')
cv2.namedWindow('thresholded')
cv2.namedWindow('thresholded-2')
cv2.namedWindow("temp")
ST.SetTrackBarsRed()
ST.SetTrackBarsBlue()
ST.SetTrackBarsKernel()

#First Frame

vc = CamLib.WebcamVideoStream(src = 0).start()#cv2.VideoCapture(0)


frame = vc.read()
distance2Line = 0
lastdistance = 0
#Main Loop
while True:

	start = time.time()
	#frame=cv2.resize(frame,(320,240)) #Reduce the resolution
	zero_num=15 #zeros to be padded
	#edges3 = cv2.Canny(frame,150,300)
##    thresh=cv2.dilate(thresh,kernel2,iterations=2)


	#frame = cv2.copyMakeBorder(frame,zero_num,zero_num,zero_num,zero_num,cv2.BORDER_CONSTANT,value=[0,0,0])


	#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR to HSV conversion
	#end = time.time()
	#print("Borders and Conversions. Time:",(end-start))

	# get current positions of trackbars 
	hl= cv2.getTrackbarPos('Hlow','controller')
	sl= cv2.getTrackbarPos('Slow','controller')
	vl= cv2.getTrackbarPos('Vlow','controller')
	hh= cv2.getTrackbarPos('Hhigh','controller')
	sh= cv2.getTrackbarPos('Shigh','controller')
	vh= cv2.getTrackbarPos('Vhigh','controller')

	# get current positions of trackbars second
	hl2= cv2.getTrackbarPos('Hlow','controller-2')
	sl2= cv2.getTrackbarPos('Slow','controller-2')
	vl2= cv2.getTrackbarPos('Vlow','controller-2')
	hh2= cv2.getTrackbarPos('Hhigh','controller-2')
	sh2= cv2.getTrackbarPos('Shigh','controller-2')
	vh2= cv2.getTrackbarPos('Vhigh','controller-2')

	print hl,sl,vl
	end = time.time()
	#print("Trackbars are read. Time:",(end-start))
	#Create the kernel
	
	ker_size=cv2.getTrackbarPos('Kernel Size','controller')
	ker_size2=cv2.getTrackbarPos('Kernel2 Size','controller')

	h=np.kaiser(ker_size,1)
	kernel=np.sqrt(np.outer(h,h))

	h=np.kaiser(ker_size2,1)
	kernel2=np.sqrt(np.outer(h,h))

	low=np.array([hl,sl,vl], dtype=np.uint8) #Lower limits
	high=np.array([hh,sh,vh], dtype=np.uint8) #Upper limits

	low2=np.array([hl2,sl2,vl2], dtype=np.uint8) #Lower limits-2
	high2=np.array([hh2,sh2,vh2], dtype=np.uint8) #Upper limits-2

	thresh=cv2.inRange(hsv, low, high) #Thresholded image
	thresh2=cv2.inRange(hsv, low2, high2) #Thresholded image 2
	end = time.time()
	
	#print("Thresholding. Time:",(end-start))
#Eliminating noisy points

	thresh=cv2.erode(thresh,kernel,iterations=2)
	thresh=cv2.dilate(thresh,kernel2,iterations=2)

	thresh2=cv2.erode(thresh2,kernel,iterations=2)
	thresh2=cv2.dilate(thresh2,kernel2,iterations=2)
	end = time.time()
	#print("Erode Dilate. Time:",(end-start))
#1st obj islemler    

	edges = cv2.Canny(thresh,50,200)
	contours,hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	end = time.time()
	#print("Contours are extracted. Time:",(end-start))
		
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
#        print((contours))
		
		rect = cv2.minAreaRect(listed[0])

		ellipse=cv2.fitEllipse(listed[0])

		#print(ellipse)
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

		slope = offset[1]/offset[0]

		if slope>0:
			point1=point1_obj1
		else:
			point1=point2_obj1
		cv2.circle(frame,(int(point1[0]),int(point1[1])),10,(0,0,0))
		#cv2.ellipse(frame,ellipse,(0,255,255),2)
		#print("Line Length from Ellipse: ",length*2)
		#print("Line Length from Rectangle:",norm(np.array(rect[0])-np.array(rect[1])))

		# Draw the line
		A = cv2.line(frame,(int(point1_obj1[0]),int(point1_obj1[1])),(int(point2_obj1[0]),int(point2_obj1[1])),(255,255,0),2)
		#print(A) 
	except:
		print("Object is not detected")
	end = time.time()
	#print(point1_obj1)

	#print("1st object detected. Time:",(end-start))

#2sn obj islemler
		
	edges2 = cv2.Canny(thresh2,50,200)
	contours2,hierarchy2 = cv2.findContours(edges2,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	try:
		count=0
		max_area=1000
		for cnt in contours2:
			area=cv2.contourArea(cnt)
			if area>max_area:
				count = count + 1

		if (len(contours2)>0)&(count>0):
			listed2=sorted(contours2, key=cv2.contourArea, reverse=True)
			cv2.fillConvexPoly(temp2,listed2[0],[255,0,0])
			temp2=cv2.inRange(temp2,np.array([250,0,0]),np.array([260,5,5]))

		else:
			temp2=thresh2.copy()
		temp = cv2.add(temp,temp2)
		cv2.imshow("temp", temp)
  
		
   
		ellipse=cv2.fitEllipse(listed2[0])

		# Take theta values from ellipse object
		theta_rad = np.deg2rad(ellipse[2])
		# Compose a unit vector for the line
		unitvec = [np.sin(theta_rad),-np.cos(theta_rad)]
		# Calculated the length of the line
		length = 0.5*np.sqrt(np.absolute(ellipse[1][0]*ellipse[1][0] - ellipse[1][1]*ellipse[1][1]))
		# Calculate the line points
		offset = np.multiply(unitvec,length)


		point1_obj2 = ellipse[0] + offset
		point2_obj2 = ellipse[0] - offset
		
		cv2.line(frame,(int(point1_obj2[0]),int(point1_obj2[1])),(int(point2_obj2[0]),int(point2_obj2[1])),(0,0,255),2)
		temp3 = cv2.add(temp , temp2)
		
	except:
		print("Object is not detected")
	end = time.time()
	

	#print("2nd object detected. Time:",(end-start))
#Original and Thresholded Images
	
	cv2.imshow("Original Image", frame)    
	cv2.imshow("thresholded", thresh)
	cv2.imshow("thresholded-2", thresh2)
	
   # cv2.imshow("edges", edges3)

	#pts = cv2.ellipse2Poly(ellipse)

#    print(ellipse)


## New Frame is taken after all operations
	frame = vc.read()
## Is ESC pressed ( Exit Request)
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break


## Distance to line from the barge point

	try:
		distance2Line = -cv2.pointPolygonTest(listed2[0],(point1[0],point1[1]),True)
		pass
		#distance2Line = #norm(np.cross(point1_obj2-point1,point2_obj2-point1))/norm(point2_obj2-point1_obj2)    
	except:
		
	#print("Neden?")
		pass
	print("Distance...." , (distance2Line+lastdistance)/2)

	end = time.time()
	lastdistance = distance2Line;

	
	print("Execution Time",(end-start))

	

