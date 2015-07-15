import urllib
import sqlite3

PTZ_STOP=1
TILT_UP=0
TILT_UP_STOP=1
TILT_DOWN=2
TILT_DOWN_STOP=3
PAN_LEFT=4
PAN_LEFT_STOP=5
PAN_RIGHT=6
PAN_RIGHT_STOP=7
PTZ_LEFT_UP=90
PTZ_RIGHT_UP=91
PTZ_LEFT_DOWN=92
PTZ_RIGHT_DOWN=93
PTZ_CENTER=25
PTZ_VPATROL=26
PTZ_VPATROL_STOP=27
PTZ_HPATROL=28
PTZ_HPATROL_STOP=29

#Get password for database
conn = sqlite3.connect('/home/john/opencv_database.db')
c = conn.cursor()
passCode = c.execute('select password from passwords limit 1;')
for passWd in passCode:
	passWd = str(passWd)
	passWd = passWd[3:len(passWd)-3]

urllib.urlopen("http://admin:" + passWd + "@10.0.0.6:8090/decoder_control.cgi?command=4")

urllib.urlopen("http://admin:" + passWd + "@10.0.0.6:8090/decoder_control.cgi?command=1")
