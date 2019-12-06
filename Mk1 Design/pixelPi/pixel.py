from bitstring import BitArray
import math
import Node
import BLE
import csv

xpos_len = 4 # 4 bits -> 0-15
xpos_start = 0 # x starts at bit 0 in x+y bits
ypos_len = 4 # 4 bits -> 0-15
ypos_start = xpos_len # y starts at bit len(xpos in bits) in x+y bits
xy_len = xpos_len + ypos_len # total lengh of x+y bits
message_length = 20 * 8 # in bits
group_id_len = 4 # bits used for group id
group_size = math.floor((message_length-group_id_len) / xy_len) # currently 19

def decodeMessages(messages):
	''' Function to decode seat positions for sending via message_length BLE broadcasts
	Args:
	@messages (array of BitArrays): Should contain all the arrays of from encodeMessages

	Returns:
	@students (array of int tuples): Format is [id, x, y]
	'''
    students = []
    for message in messages:
        message_bytes = message.tobytes()
        group_num = int(message_bytes[0])>>4
        for i in range(0, len(message.tobytes()) - 1):
            byte1 = message_bytes[i]
            byte2 = message_bytes[i+1]
            students.append((group_num*i + i, int(byte1)&0b1111, int(byte2)>>4))
    return students

with open('settings.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	print(row['first_name'], row['last_name'])