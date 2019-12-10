import csv

settings_address = "/home/pi/settings.csv"

L = 1
X = -1 
Y = -1
myID = -1 

with open(settings_address, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        myID = int(row['ID'])

L = 1
f = open(settings_address, "w")
f.write(f"L,X,Y,ID\n{L},{X},{Y},{myID}")
f.close()
    
