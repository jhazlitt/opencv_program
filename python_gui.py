import sqlite3
from Tkinter import *

class MyApp:
	def __init__(self, parent):
		self.frame = Frame(parent)
		self.frame.pack()
		
		self.home()

	def home(self):
		# Remove all widgets from the frame
		self.clearFrame()

		# Add new widgets to the frame
		self.testButton = Button(self.frame, text="text", command=self.addCamera)

		# Position the widgets
		self.testButton.grid(row=0)
		
	def addCamera(self):
		# Remove all widgets from the frame
		self.clearFrame()

		# Add new widgets to the frame
		self.nameLabel = Label(self.frame, text="Camera name:") 
		self.ipLabel = Label(self.frame, text="IP address:")
		self.portLabel = Label(self.frame, text="Port:")
		self.passwordLabel = Label(self.frame, text="Password:")
		self.nameEntry = Entry(self.frame)
		self.ipEntry = Entry(self.frame)
		self.portEntry = Entry(self.frame)
		self.passwordEntry = Entry(self.frame)
		self.addCameraButton = Button(self.frame, text="Add", command=self.writeCameraToDatabase)
		
		# Position the widgets
		self.nameLabel.grid(row=0, sticky=E) 
		self.ipLabel.grid(row=1, sticky=E)
		self.portLabel.grid(row=2, sticky=E)
		self.passwordLabel.grid(row=3, sticky=E)
		self.nameEntry.grid(row=0, column=1)
		self.ipEntry.grid(row=1, column=1)
		self.portEntry.grid(row=2, column=1)
		self.passwordEntry.grid(row=3, column=1)
		self.addCameraButton.grid(row=4, columnspan=2)

	def clearFrame(self):
		for widget in self.frame.winfo_children():
			widget.destroy()

	def writeCameraToDatabase(self):
		name = self.nameEntry.get()
		ip = self.ipEntry.get()
		port = self.portEntry.get()
		password = self.passwordEntry.get()
		
		c.execute('INSERT INTO cameras (name, ip, port, password) VALUES ("' + name + '", "' + ip + '", "' + port + '", "' + password + '");')
		conn.commit()
		self.home()

# Connect to database
conn = sqlite3.connect('/home/john/opencv_database.db')
c = conn.cursor()

# Create application window
root = Tk()
root.title("security.py")
root.minsize(width=640, height=480)
myApp = MyApp(root)
root.mainloop()
