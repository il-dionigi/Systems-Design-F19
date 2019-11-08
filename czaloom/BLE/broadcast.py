import os

os.system("sudo hciconfig hci0 up")
os.system("sudo hciconfig hci0 leadv 3")

UUID = "ab c4" # Max 4 bytes (in hex)
ServiceID = "cf de" # Max 4 bytes (in hex)
msg = "zabcdefghijklmnopqrs" # Max 20 bytes (char)

print(len(msg))

dif = 20 - len(msg)
maxSizeMajor = 31
maxSizeMinor = 23

if(dif > 0):
	maxSizeMinor = maxSizeMinor - dif
	maxSizeMajor = maxSizeMajor - dif

SizeMajor = str(hex(maxSizeMajor))
SizeMinor = str(hex(maxSizeMinor))

preamble = "sudo hcitool -i hci0 cmd 0x08 0x0008 "
preamble = preamble + SizeMajor[2] + SizeMajor[3]
preamble = preamble + " 02 "
preamble = preamble + "01 06 " #Configureable  (Flag type, flag data)
preamble = preamble + "03 "
preamble = preamble + "03 "
preamble = preamble + UUID + " " #Configureable (Service data type, MUUID, MUUID)
preamble = preamble + SizeMinor[2] + SizeMinor[3]
preamble = preamble	+ " 16 "
preamble = preamble + ServiceID + " " # (Service data type, mUUID, mUUID)

command = preamble
for l in msg:
	hexnum = str(hex(ord(l)))
	command = command + hexnum[2] + hexnum[3] + " "

for i in range(dif):
	command = command + "00 "

print(command)