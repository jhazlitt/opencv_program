import numpy as np
import cv2
import sqlite3

#Get password for database
conn = sqlite3.connect('/home/john/opencv_database.db')
c = conn.cursor()
passCode = c.execute('select password from passwords limit 1;')
for passWd in passCode:
	passWd = str(passWd)
	passWd = passWd[3:len(passWd)-3]

#Capture video
cap = cv2.VideoCapture("http://10.0.0.6:8090/videostream.asf?user=admin&pwd=" + passWd + "&resolution=32&rate=0&.mpg")

fgbg = cv2.BackgroundSubtractorMOG()

while(1):
	ret, frame = cap.read()
	print frame.shape	
	fgmask = fgbg.apply(frame)
	
	kernel = np.ones((5,5),np.uint8)	
	fgmask = cv2.erode(fgmask,kernel,iterations = 1)
#	fgmask = cv2.dilate(fgmask,kernel,iterations = 1)
	
	contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
#	cnt = contours[0]
	try:
		cnt = contours[0]
		x,y,w,h = cv2.boundingRect(cnt)
		minX = x
		minY = y
		maxX = x + w
		maxY = y + h
		for contour in contours:
			x,y,w,h = cv2.boundingRect(contour)
			if x < minX:
				minX = x
			elif y < minY:
				minY = y
			elif (x + w) > maxX:
				maxX = (x + w)
			elif (y + h) > maxY:
				maxY = (y + h)

		cv2.rectangle(fgmask,(minX,minY),(maxX,maxY),(255,255,255),3)
	except:
		continue
	
	cv2.imshow('frame',fgmask)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
