#from bitstring import BitArray
import math
import Node
import BLE
import csv
import board
import neopixel
import IRModule
import RPi.GPIO as GPIO
import time
import routines

pixels = neopixel.NeoPixel(board.D18, 12)

myID = 2

xpos_len = 4 # 4 bits -> 0-15
xpos_start = 0 # x starts at bit 0 in x+y bits
ypos_len = 4 # 4 bits -> 0-15
ypos_start = xpos_len # y starts at bit len(xpos in bits) in x+y bits
xy_len = xpos_len + ypos_len # total lengh of x+y bits
message_length = 20 * 8 # in bits
group_id_len = 4 # bits used for group id
group_size = math.floor((message_length-group_id_len) / xy_len) # currently 19

# set up IR pi pin and IR remote object
irPin = 16
ir = IRModule.IRRemote(callback='DECODE')
# using 'DECODE' option for callback will print out
# the IR code received in hexadecimal
# this can used to get the codes for whichever NEC
# compatable remote you are using

# set up GPIO options and set callback function required
# by the IR remote module (ir.pWidth)        
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
GPIO.setup(irPin,GPIO.IN)   # set irPin to input
GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

routine = -1

def remote_callback(code):
	global routine
	# Codes listed below are for the
	# Sparkfun 9 button remote

	if code == 16582903:
		print("Pressed: 1")
		routine = 1

	elif code == 16615543:
		print("Pressed: 2")
		routine = 2
		
	elif code == 16605343:
		print("Pressed: 3")
		routine = 3

	elif code == 16591063:
		print("Pressed: 4")
		routine = 4

	elif code == 16623703:
		print("Pressed: 5")
		routine = 5

	elif code == 16607383:
		print("Pressed: 6")
		routine = 6

	elif code == 16586983:
		print("Pressed: 7")
		routine = 7

	elif code == 16619623:
		print("Pressed: 8")
		routine = 8

	elif code == 16603303:
		print("Pressed: 9")
		routine = 9

	elif code == 16593103:
		print("Pressed: 0")
		routine = 0

	elif code == 16599223:
		print("Pressed: Stop")
		routine = -1

	else:
		print("Pressed: Stop")
		routine = -1
	return

# turn off verbose option and change callback function
# to the function created above - remote_callback()
ir.set_verbose(False)
ir.set_callback(remote_callback)

def decodeMessages(messages):
	chunks, chunksize = math.ceil(len(messages)/20), 20
	messages = [messages[i:i+chunksize] for i in range(0,len(messages),chunksize)]

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

def getNewCoords():
	global Coords
	global ListenFlag

	positions = decodeMessages(BLE.listen())
	#Work on this
	for i in range(len(positions)):
		if myID is positions[i][0]:
			myCoords = positions[i]
			Coords = (myCoords[1], myCoords[2])
			ListenFlag = 0
			f = open("settings.csv", "w")
			f.write(f"L,X,Y\n{ListenFlag},{X},{Y}")
			f.close()
	return

Coords = (-1,-1)
ListenFlag = 1

with open('settings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		ListenFlag = int(row['L'])
		Coords = (int(row['X']), int(row['Y']))

pixels.fill((0, 0, 255))

while ListenFlag:
	getNewCoords()
	with open('settings.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			ListenFlag = int(row['L'])
			Coords = (int(row['X']), int(row['Y']))

pixels.fill((0, 255, 0))
time.sleep(5)
pixels.fill((0, 0, 0))

try:    
	max_dim = (3,3) # Need to actually find this
	gradient = (math.ceil(255/(max_dim[0]-1)), math.ceil(255/(max_dim[1]-1)))

	# This is where you could do other stuff
	# Blink a light, turn a motor, run a webserver
	# count sheep or mine bitcoin
	while True:
		if ListenFlag:
			getNewCoords()
		if routine == 0:
			ListenFlag = 1
		elif routine == 1:
			for loop in range(5):
				for i in range(max_dim[0]):
					routines.horizontal_scroll(i,coords,max_dim,gradient)
					time.sleep(0.25)
		elif routine == 2:
			for loop in range(5):
				for i in range(max_dim[1]):
					routines.vertical_scroll(i,coords,max_dim,gradient)
					time.sleep(0.25)
		else:
			pixels.fill((0, 0, 0))
			time.sleep(1)
	  
except:
	ir.remove_callback()
	GPIO.cleanup(irPin)



