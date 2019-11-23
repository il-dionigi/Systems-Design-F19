from PyQt5 import QtCore, QtGui, QtWidgets #works for pyqt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import pibake
import sys

class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("ui/mainapp.ui", self)

#These functions read from the card
def write_role_id(role_id, drive):
	f = open('image_dir/role_id.txt', 'w+')
	#f = open(str(drive)[0] + str()
	f.write(str(role_id))
	f.close()
	return 0

def read_role_id():
	try:
		f = open('image_dir/role_id.txt', 'r')
		role_id = f.read()
		return int(role_id)
	except:
		return -1
#The above functions read from the card

def write_rbp_image(DriveLabel):
	iso_image = 'image_dir/image.iso'
	iso_dir = str(DriveLabel) + str(iso_image)
	return 0
	#Do something to write the image

def handle_role_read(role_id, window):
	window.readRoleText.setText(str(role_id))
	#return 0



if __name__ == "__main__":
	#Form, Window = uic.loadUiType("ui/mainapp.ui")
	app = QApplication([])
	window = Window()
	#form = Form()
	#form.setupUi(window)

	#Initialize Window callbacks.
	#window.RoleIdText.textchanged.connect()
	window.WriteRole.clicked.connect(lambda: write_role_id(window.RoleIdText.text(), window.DriveLabelText.text()))
	window.WriteImage.clicked.connect(lambda: write_rbp_image(window.DriveLabelText.text()))
	window.ReadRole.clicked.connect(lambda: handle_role_read(read_role_id(), window))

	window.show()
	sys.exit(app.exec_())