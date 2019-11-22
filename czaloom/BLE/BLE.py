from btle import Scanner, DefaultDelegate
import os
import math
import time 
import numpy as np

# --- START OF BROADCAST DEFINITIONS ---

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

def BLE_broadcast_setup():
	os.system("sudo hciconfig hci0 up")
	os.system("sudo hciconfig hci0 leadv 3")
	return

def BLE_broadcast(data, UUID = "ABC4", Number_of_Broadcast_Cycles = 3, Time_Between_Transmissions = 15):
	# Broadcasts data in 20 byte payloads over Number_of_Broadcast_Cycles with a Time_Between_Transmissions in seconds
	# UUID is a device identifier, should be 2 bytes no spaces. May be changed if signal is relayed.
	UUID = str(UUID[0:2]) + " " + str(UUID[2:4]) # Max 4 bytes (in hex)
	msg = data

	number_of_messages = int(math.ceil(len(msg) / 20.0))
	if len(msg) % 20 != 0:
		for i in range(20 - len(msg) % 20):
			msg = msg + "_"

	state = "Transmitting " + str(number_of_messages) + " messages"
	print(state)

	ServiceID_ = " " + int_to_byte(number_of_messages) + " "

	#Add automatic message and id parsing here

	preamble = "sudo hcitool -i hci0 cmd 0x08 0x0008 1f 02 01 06 03 03 "
	preamble = preamble + UUID #Configureable (Service data type, MUUID, MUUID)
	preamble = preamble + " 23 16 "

	for iteration in range(Number_of_Broadcast_Cycles):
		for i in range(number_of_messages):

			ServiceID = int_to_byte(i+1) + ServiceID_
			ServiceID = UUID
			command = preamble + ServiceID
			for l in msg[i*20:i*20+20]:
				hexnum = str(hex(ord(l)))
				command = command + hexnum[2] + hexnum[3] + " "

			#print(command) # Uncomment if not on Pi
			os.system(command) # Uncomment if on Pi
			time.sleep(Time_Between_Transmissions)

# --- END OF BROADCAST DEFINITIONS ---

# --- START OF LISTEN DEFINITIONS ---

def charhex_to_int(c):
    if c == 'A' or c == 'a':
        return 10
    elif c == 'B' or c == 'b':
        return 11
    elif c == 'C' or c == 'c':
        return 12
    elif c == 'D' or c == 'd':
        return 13
    elif c == 'E' or c == 'e':
        return 14
    elif c == 'F' or c == 'f':
        return 15
    else:
        return int(c)

def get_letter(s):
    ascii_ = 16*charhex_to_int(s[0]) + charhex_to_int(s[1])
    return chr(ascii_)
def get_number(s):
    return 16*charhex_to_int(s[0]) + charhex_to_int(s[1])

def get_ID(s):
    return [get_number(s[0:2]),get_number(s[2:4])]
def get_Message(s):
    MSG = ""
    for i in range(4,30,2):
        MSG = MSG + get_letter(s[i:i+2])
    return MSG

def is_new_message(id_, id_list):
    m_id = id_[0]
    m_total = id_[1]
    if m_total == 0:
        return 0
    for i in id_list:
        if i == m_id:
            return 0
    return 1

class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self) 

def BLE_listen(UUID = "ABC4"):
	UUID = UUID[2:4] + UUID[0:2]
	scanner = Scanner().withDelegate(ScanDelegate())

	id_list = []
	msg_arr = []
	start_flag = 1
	max_num_messages = 0
	message_count = 0

	while(1):
	    devices = scanner.scan(10.0)

	    for dev in devices:
	        id_ = [0,0]
	        found_flag = 0
	        for (adtype, desc, packet) in dev.getScanData():
	            if desc == "Complete 16b Services":
	                if packet[4:8] == master_pi_UUID:
	                    found_flag = 1
	            if desc == "16b Service Data" and found_flag:
	                id_ = get_ID(packet)
	        if is_new_message(id_, id_list) and found_flag:
	            if start_flag:
	                max_num_messages = id_[1]
	                start_flag = 0
	                id_list = [None] * max_num_messages
	                msg_arr = [None] * max_num_messages
	            id_list[id_[0]] = m_id
	            msg_arr[id_[0]] = get_Message(packet)
	            message_count = message_count + 1
	    if message_count == max_num_messages:
	        break

	message = ""
	for i in msg_arr:
	    message = message + i

	return message

# --- END OF LISTEN DEFINITIONS ---


#BLE_broadcast_setup()
#BLE_broadcast("Hello! This is our ECE180DA Project!")
BLE_broadcast("AAAAABBBBBAAAAABBBBB")

#print(BLE_listen())
