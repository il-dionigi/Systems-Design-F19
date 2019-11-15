from bluepy.btle import Scanner, DefaultDelegate
import math
import numpy as np

#See BLE_scan.py for source

# - SETTINGS - 
master_pi_address = "b8:27:eb:28:ee:43" #Richard's BLE Address
master_pi_UUID = "c4ab"
# ------------

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

scanner = Scanner().withDelegate(ScanDelegate())

id_list = []
msg_arr = []
start_flag = 1
max_num_messages = 0
message_count = 0

while(1):
    devices = scanner.scan(10.0)

    for dev in devices:
            #Method 2
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

print(message)





                    
    			
