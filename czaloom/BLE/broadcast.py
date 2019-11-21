import os
import math
import time 

#os.system("sudo hciconfig hci0 up")
#os.system("sudo hciconfig hci0 leadv 3")

UUID = "ab c4" # Max 4 bytes (in hex)

msg  = str(raw_input())

number_of_messages = int(math.ceil(len(msg) / 20.0))
if len(msg) % 20 != 0:
	for i in range(20 - len(msg) % 20):
		msg = msg + "_"

state = "Transmitting " + str(number_of_messages) + " messages"
print(state)

def hex_to_char(c):
	if c < 10:
		return str(c)
	elif c == 10:
		return "a"
	elif c == 11:
		return "b"
	elif c == 12:
		return "c"
	elif c == 13:
		return "d"	
	elif c == 14:
		return "e"
	elif c == 15:
		return "f"
	else:
		return "0"

def int_to_byte(x):
	byte = ""
	if(x < 16):
		byte = "0" + hex_to_char(x)
	else:
		byte = hex_to_char(int(x / 16)) + hex_to_char(x % 16)
	return byte

ServiceID_ = " " + int_to_byte(number_of_messages) + " "

#Add automatic message and id parsing here

preamble = "sudo hcitool -i hci0 cmd 0x08 0x0008 1f 02 01 06 03 03 "
preamble = preamble + UUID #Configureable (Service data type, MUUID, MUUID)
preamble = preamble + " 23 16 "

for i in range(number_of_messages):

	ServiceID = int_to_byte(i+1) + ServiceID_
	ServiceID = UUID
	command = preamble + ServiceID
	for l in msg[i*20:i*20+20]:
		hexnum = str(hex(ord(l)))
		command = command + hexnum[2] + hexnum[3] + " "

	#print(command) # Uncomment if not on Pi
	os.system(command) # Uncomment if on Pi
	time.sleep(5)
