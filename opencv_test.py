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

while(True):
	ret, frame= cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	cv2.imshow('frame',gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
