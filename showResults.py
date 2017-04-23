import cv2
import numpy as np

#Windows
cv2.namedWindow("Original Image")
cv2.namedWindow('controller')
cv2.namedWindow('controller-2')
cv2.namedWindow('thresholded')
cv2.namedWindow('thresholded-2')
cv2.namedWindow("temp")

fourcc = cv2.cv.CV_FOURCC('H','2','6','1')
out = cv2.VideoWriter()
success = out.open('output.avi',fourcc,5.0,(352,288),1)   

frame = 0
def showRes(updatedframe,dummy):
	cv2.imshow("temp",updatedframe)	
	out.write(updatedframe)