from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
        def __init__(self):
                DefaultDelegate.__init__(self) 

        #def handleDiscovery(self,dev,isNewDev,isNewData):
                #if isNewDev:
                        #print("Discovered Device" , dev.addr)
                #elif isNewData:
                        #print("Recieved New Data from" , dev.addr)
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
        if dev.addr == "b8:27:eb:28:ee:43":
		print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        	for (adtype, desc, value) in dev.getScanData():
       			print("  %s = %s" % (desc, value))
			print(value)
