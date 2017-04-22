import ThreadedWebcam as CamLib
from copy import deepcopy
from Tkinter import * 
import cv2
import numpy as np
import time
import pylab
from numpy import linalg
from numpy.linalg import norm
import SetTrackBar as ST
import DetectBlue as DB
import DetectRed as DR
import OzHasekiSerial as Ser
import threading

import OzHasekiSerial as Ser


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


distance2Line = 0
lastdistance = 0
zero_num=15 #zeros to be padded
#textboxthread = threading.Thread(target=DistanceTxt.mainloop())
SerCom = threading.Thread(target=Ser.ComLoop,args=(distance2Line,lastdistance))

#Main Loop
while True:

	start = time.time()
	frame = vc.read()
	frame=cv2.resize(frame,(322,258)) #Reduce the resolution
	cv2.imshow("Original Image",frame)
	frame = cv2.copyMakeBorder(frame,zero_num,zero_num,zero_num,zero_num,cv2.BORDER_CONSTANT,value=[0,0,0])
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR to HSV conversion

	frameb = deepcopy(frame)
	framer = deepcopy(frame)
	hsvr = deepcopy(hsv)
	hsvb = deepcopy(hsv)

	Bthread = threading.Thread(target=DB.FindBlueObject,args=(frame,frameb,hsvb))
	Rthread = threading.Thread(target=DR.FindRedObject,args=(frame,framer,hsvr))

	#DR.FindRedObject(framer,hsvr)
	Bthread.start()
	Rthread.start()

	Bthread.join()
	Rthread.join()
	SerCom.start()

##### Threads are joined here. 

##### TODO: Threads will be created. 
##### TODO: frame,hsv will be deepcopied
##### TODO: CPU Affinity will be researched

## New Frame is taken after all operations
## Is ESC pressed ( Exit Request)
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break


	if(isinstance(ST.RedList, np.ndarray) and isinstance(ST.BlueList, list)):
		ST.distance2Line = -cv2.pointPolygonTest(ST.BlueList[0],(ST.RedList[0],ST.RedList[1]),True)


## Distance to line from the barge point
	try:

		ST.distance2Line = -cv2.pointPolygonTest(ST.BlueList[0],(ST.RedList[0],ST.RedList[1]),True)
		print("Distance...." , (ST.distance2Line+lastdistance)/2)
		lastdistance = ST.distance2Line;
		pass
		#distance2Line = #norm(np.cross(point1_obj2-point1,point2_obj2-point1))/norm(point2_obj2-point1_obj2)    
	except:
		pass
	
	#Txt.insert(END,str(distance2Line))
	#textboxthread.start()
	end = time.time()

	
	print("Execution Time",(end-start))

	

