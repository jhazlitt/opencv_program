import numpy as np
import cv2
import sqlite3
import urllib
import time
import os

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

# Get the starting time and starting video number
startTime = time.time()
videoNumber = 1

# Codec and VideoWriter object for saving the video
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter(str(videoNumber) + '.avi',fourcc, 15, (640,480))

fgbg = cv2.BackgroundSubtractorMOG()

motionDetectedFrameCount = 0
motionDetected = False
mute = False
# While the camera is recording
while(1):
	# Check for any keys that were pressed
	k = cv2.waitKey(30) & 0xff
	if k == ord('q'):
		break
	elif k == ord('k'):
		# Generate a new background
		fgbg = cv2.BackgroundSubtractorMOG()
	elif k == ord('m'):
		mute = not mute 
	
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

	# If there are no contours an error will be thrown.  If there are contours:
	if len(contours) != 0:
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
		motionDetected = True
		if mute == False:
			os.system("aplay beep.wav")

		# Record movement time of occurrence in log
		f = open('log.txt','a')
		f.write('Movement detected ' + time.asctime(time.localtime()) + '\n')
		f.close()

	endTime = time.time() 
	print "endTime: " + str(endTime)
	elapsedTime = endTime - startTime
	print "elapsedTime: " + str(elapsedTime)

	# Put a timestamp on the video frame
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame,str(time.asctime(time.localtime())),(0,25), font, 1, (0,0,0), 7)
	cv2.putText(frame,str(time.asctime(time.localtime())),(0,25), font, 1, (255,255,255), 2)

	cv2.imshow('Video',frame)
	out.write(frame)

	# Save the video after a specified number of seconds
	if elapsedTime >= 60:
		out.release()
		
		# If there was motion detected during the recording, move on to the next video number.  Otherwise write over this video

		# If there are more than a specified number of videos, the count is set back to 1 so they can all be written over
		if (videoNumber == 150) and (motionDetected == True):
			motionDetected = False
			videoNumber = 1
		elif motionDetected == True:
			motionDetected = False
			videoNumber += 1

		out = cv2.VideoWriter(str(videoNumber) + '.avi',fourcc, 12, (640,480))
		startTime = time.time()
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
