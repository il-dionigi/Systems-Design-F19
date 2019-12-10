settings_address = "/home/pi/settins.csv"

L = 1
X = -1 
Y = -1
myID = -1 

with open(settings_address, newline='') as csvfile:
    pixels.fill((155,0,0))
    reader = csv.DictReader(csvfile)
    for row in reader:
        myID = int(row['ID'])

L = 1
f = open(settings_address, "w")
f.write(f"L,X,Y,ID\n{ListenFlag},{Coords[0]},{Coords[1]},{myID}")
f.close()
    
