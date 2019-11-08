import os

os.system("sudo hciconfig hci0 up")
os.system("sudo hciconfig hci0 leadv 3")
# If this fails to work, run apt-get update and upgrade
