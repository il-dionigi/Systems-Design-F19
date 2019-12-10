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
import encoder

pixels = neopixel.NeoPixel(board.D18, 12)

myID = 1
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
		for loop in range(5):
				for i in range(max_dim[0]):
					routines.horizontal_scroll(pixels,i,Coords,max_dim,gradient)
					time.sleep(2)
		# routine = 1

	elif code == 16615543:
		print("Pressed: 2")
		for loop in range(5):
				for i in range(max_dim[1]):
					routines.vertical_scroll(pixels,i,Coords,max_dim,gradient)
					time.sleep(2)
		# routine = 2
		
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
		routine = -2
	return

# turn off verbose option and change callback function
# to the function created above - remote_callback()
ir.set_verbose(False)
ir.set_callback(remote_callback)

def getNewCoords():
	global Coords
	global ListenFlag
	temp = BLE.listen()
	temp = temp.replace('_', '')
	print(temp)
	positions = encoder.decodeMessage(temp)
	#Work on this
	for i in range(len(positions)):
		if myID is positions[i][0]:
			myCoords = positions[i]
			Coords = (myCoords[1], myCoords[2])
			ListenFlag = 0
			f = open("settings.csv", "w")
			f.write(f"L,X,Y\n{ListenFlag},{Coords[0]},{Coords[1]}")
			f.close()
	routine = -1
	return

Coords = (-1,-1)
ListenFlag = 1

with open('settings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		ListenFlag = int(row['L'])
		Coords = (int(row['X']), int(row['Y']))

pixels.fill((0, 0, 155))

while ListenFlag:
	getNewCoords()
	with open('settings.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			ListenFlag = int(row['L'])
			Coords = (int(row['X']), int(row['Y']))
	print(routine)
	time.sleep(1)

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
					routines.horizontal_scroll(pixels,i,Coords,max_dim,gradient)
					time.sleep(0.25)
			routine = -1
		elif routine == 2:
			for loop in range(5):
				for i in range(max_dim[1]):
					routines.vertical_scroll(pixels,i,Coords,max_dim,gradient)
					time.sleep(0.25)
			routine = -1
		else:
			pixels.fill((0, 0, 0))
			time.sleep(1)

except Exception as e:
	print(e)
	ir.remove_callback()
	GPIO.cleanup(irPin)



