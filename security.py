import numpy as np
import cv2
import sqlite3
import urllib
import datetime

# Get password for database
conn = sqlite3.connect('/home/john/opencv_database.db')
c = conn.cursor()
passCode = c.execute('select password from passwords limit 1;')

# Strip extra characters from the query result
for passWd in passCode:
	passWd = str(passWd)
	passWd = passWd[3:len(passWd)-3]

# Specify the video to be captured
cap = cv2.VideoCapture("http://10.0.0.6:8090/videostream.asf?user=admin&pwd=" + passWd + "&resolution=32&rate=0&.mpg")

# Codec and VideoWriter object for saving the video
i = datetime.datetime.now()
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('' + str(i) + '.avi',fourcc, 12, (640,480))

fgbg = cv2.BackgroundSubtractorMOG()

# Get the starting time
i = datetime.datetime.now()
startTime = i.hour + i.minute + i.second	
print "startTime: " + str(startTime)

motionDetectedFrameCount = 0
# While the camera is recording
while(1):
	# Check for any keys that were pressed
	k = cv2.waitKey(30) & 0xff
	if k == ord('q'):
		break
	elif k == ord('k'):
		# Generate a new background
		fgbg = cv2.BackgroundSubtractorMOG()
	
	# Read the current frame from the camera
	ret, frame = cap.read()

	# If there has been motion detected for more than a specified number of frames, generate a new mask
	if motionDetectedFrameCount > 1:
		fgbg = cv2.BackgroundSubtractorMOG()
		motionDetectedFrameCount = 0

	# Apply the mask to the frame
	fgmask = fgbg.apply(frame)
	kernel = np.ones((5,5),np.uint8)	
	fgmask = cv2.erode(fgmask,kernel,iterations = 1)
	fgmask = cv2.dilate(fgmask,kernel,iterations = 2)
	
	# Find differences between the mask and frame, if any.  These are called contours
	contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

	cv2.imshow('Video',frame)
	
	# If there are no contours an error will be thrown, so try to run the following code
	print len(contours)
	if len(contours) <= 1:
		endTime = i.hour + i.minute + i.second	
		print "endTime: " + str(endTime)
		elapsedTime = endTime - startTime
		print "elapsedTime: " + str(elapsedTime)
	else:
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
		cv2.rectangle(frame,(centerX,centerY),(centerX,centerY),(255,000,255),2)
		cv2.rectangle(frame,(minX,minY),(maxX,maxY),(255,000,255),2)
		motionDetectedFrameCount += 1

		endTime = i.hour + i.minute + i.second	
		print "endTime: " + str(endTime)
		elapsedTime = endTime - startTime
		print "elapsedTime: " + str(elapsedTime)
#	if elapsedTime >= 000500:
#		out.release()
#		out = cv2.VideoWriter('' + str(i) + '.avi',fourcc, 12, (640,480))
#		startTime = i.hour + i.minute + i.second

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
