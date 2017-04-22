
import cv2
BlueList =0
RedList =0
distance2Line = 0
differenceLine = 0
## Anisi var lutfen silmeyiniz
def nothing(x):
	pass

def SetTrackBarsRed():
	cv2.createTrackbar('Hlow','controller',0,179,nothing)
	cv2.createTrackbar('Hhigh','controller',0,179,nothing)

	cv2.createTrackbar('Slow','controller',0,255,nothing)
	cv2.createTrackbar('Shigh','controller',0,255,nothing)

	cv2.createTrackbar('Vlow','controller',0,255,nothing)
	cv2.createTrackbar('Vhigh','controller',0,255,nothing)

	cv2.setTrackbarPos('Hhigh','controller',15)
	cv2.setTrackbarPos('Shigh','controller',255)
	cv2.setTrackbarPos('Vhigh','controller',255)
	cv2.setTrackbarPos('Hlow','controller',0)
	cv2.setTrackbarPos('Vlow','controller',62)
	cv2.setTrackbarPos('Slow','controller',93)


def SetTrackBarsKernel():
	#Kernel
	cv2.createTrackbar('Kernel Size','controller',1,15,nothing)
	cv2.setTrackbarPos('Kernel Size','controller',3)
	cv2.createTrackbar('Kernel2 Size','controller',1,15,nothing)
	cv2.setTrackbarPos('Kernel2 Size','controller',12)

# create trackbars for 1st obj



# Trackbars for second object
def SetTrackBarsBlue():

	cv2.createTrackbar('Hlow','controller-2',0,179,nothing)
	cv2.createTrackbar('Hhigh','controller-2',0,179,nothing)

	cv2.createTrackbar('Slow','controller-2',0,255,nothing)
	cv2.createTrackbar('Shigh','controller-2',0,255,nothing)

	cv2.createTrackbar('Vlow','controller-2',0,255,nothing)
	cv2.createTrackbar('Vhigh','controller-2',0,255,nothing)

	cv2.setTrackbarPos('Hhigh','controller-2',179)
	cv2.setTrackbarPos('Shigh','controller-2',255)
	cv2.setTrackbarPos('Vhigh','controller-2',255)
	cv2.setTrackbarPos('Hlow','controller-2',98)
	cv2.setTrackbarPos('Vlow','controller-2',65)
	cv2.setTrackbarPos('Slow','controller-2',112)