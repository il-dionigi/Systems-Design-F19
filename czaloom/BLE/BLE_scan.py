import os
import time

for i in range(99):
	os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 06 1A FF 4C 00 02 15 C7 C1 A1 BF BB 00 4C AD 87 04 9F 2D 29 17 DE D2 00 00 00 00 C8 00")
	start = time.time()
	while time.time() - start < 0.15:
     		pass

