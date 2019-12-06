import BLE

#When receives a radio message, save to file
#Then attempt to load the file

device_type = 0 #This is a receiver


def loop_listen():

def load_file(file = "save.txt"):
	if os.path.exists("myfile.dat"):
		f = open(file,"r")
		msg = f.read()
		f.close()
		return msg
	else:
		return None

def save_file(msg, file = "save.txt"):
	f = open(file, "w")
	f.write(msg, file)
	return True

if device_type == 0:
	message = load_file()