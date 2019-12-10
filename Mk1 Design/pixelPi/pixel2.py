#from bitstring import BitArray
import math
import Node
import BLE
import csv
import IRModule
import RPi.GPIO as GPIO
import time
import encoder

def getNewCoords(Coords, ListenFlag):
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
	return Coords

Coords = (-1,-1)
ListenFlag = 1

with open('settings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		ListenFlag = int(row['L'])
		Coords = (int(row['X']), int(row['Y']))

while ListenFlag:
	Coords = getNewCoords(Coords)
	with open('settings.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			ListenFlag = int(row['L'])
			Coords = (int(row['X']), int(row['Y']))
	print(routine)
	time.sleep(1)