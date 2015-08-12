import numpy as np
import cv2
import sqlite3
import urllib
import datetime

#Get password for database
conn = sqlite3.connect('/home/john/opencv_database.db')
c = conn.cursor()
passCode = c.execute('select password from passwords limit 1;')
for passWd in passCode:
	passWd = str(passWd)
	passWd = passWd[3:len(passWd)-3]

#Capture video
cap = cv2.VideoCapture("http://10.0.0.6:8090/videostream.asf?user=admin&pwd=" + passWd + "&resolution=32&rate=0&.mpg")

# Codec and VideoWriter object for saving the video
i = datetime.datetime.now()
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('' + str(i) + '.avi',fourcc, 12, (640,480))

fgbg = cv2.BackgroundSubtractorMOG()

motionDetectedFrameCount = 0

i = datetime.datetime.now()
startTime = i.hour + i.minute + i.second	
while(1):
	ret, frame = cap.read()
#	print frame.shape	
	fgmask = fgbg.apply(frame)
	
	kernel = np.ones((5,5),np.uint8)	
	fgmask = cv2.erode(fgmask,kernel,iterations = 1)
#	fgmask = cv2.dilate(fgmask,kernel,iterations = 1)
	
	contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

	k = cv2.waitKey(30) & 0xff
	if k == ord('q'):
		break
	elif k == ord('k'):
		fgbg = cv2.BackgroundSubtractorMOG()
	
	# If there has been motion detected for more than a specified number of frames, generate a new background
	if motionDetectedFrameCount > 1:
		fgbg = cv2.BackgroundSubtractorMOG()
		motionDetectedFrameCount = 0

	cv2.imshow('Video',frame)
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
		
		centerX = (minX + maxX) / 2
		centerY = (minY + maxY) / 2
		cv2.rectangle(frame,(centerX,centerY),(centerX,centerY),(255,255,255),3)
		cv2.rectangle(frame,(minX,minY),(maxX,maxY),(255,255,255),3)
		cv2.imshow('Video',frame)
		motionDetectedFrameCount += 1
		print "Frame count:"
		print motionDetectedFrameCount
	except:
		continue
	
	endTime = i.hour + i.minute + i.second	
	elapsedTime = endTime - startTime
	print "Start time:"
	print startTime
	print "End time:"
	print endTime
	print "Elapsed time:"
	print elapsedTime
	if elapsedTime >= 000500:
		out.release()
		out = cv2.VideoWriter('' + str(i) + '.avi',fourcc, 12, (640,480))
		startTime = i.hour + i.minute + i.second

	cv2.imshow('Video',frame)
	out.write(frame)
cap.release()
out.release()
cv2.destroyAllWindows()

#import urllib
#import sqlite3
#
#PTZ_STOP=1
#TILT_UP=0
#TILT_UP_STOP=1
#TILT_DOWN=2
#TILT_DOWN_STOP=3
#PAN_LEFT=4
#PAN_LEFT_STOP=5
#PAN_RIGHT=6
#PAN_RIGHT_STOP=7
#PTZ_LEFT_UP=90
#PTZ_RIGHT_UP=91
#PTZ_LEFT_DOWN=92
#PTZ_RIGHT_DOWN=93
#PTZ_CENTER=25
#PTZ_VPATROL=26
#PTZ_VPATROL_STOP=27
#PTZ_HPATROL=28
#PTZ_HPATROL_STOP=29
#
##Get password for database
#conn = sqlite3.connect('/home/john/opencv_database.db')
#c = conn.cursor()
#passCode = c.execute('select password from passwords limit 1;')
#for passWd in passCode:
#	passWd = str(passWd)
#	passWd = passWd[3:len(passWd)-3]
#
#urllib.urlopen("http://admin:" + passWd + "@10.0.0.6:8090/decoder_control.cgi?command=4")
#
#urllib.urlopen("http://admin:" + passWd + "@10.0.0.6:8090/decoder_control.cgi?command=1")
