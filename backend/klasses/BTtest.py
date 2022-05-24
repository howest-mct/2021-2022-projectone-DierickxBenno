from RPi import GPIO
from SerCom import SerCom
import time
from BTconfig import BTconfig

channel = "hci0"
mac = "78:21:84:7D:85:BE"

BT = BTconfig(channel, mac)
BT.open_connection()

DogBit = SerCom("rfcomm0")
time.sleep(1)

data = [0, 0, 0]

while 1:
	print("-")
	
	data[0] = (float(DogBit.recv()))

	print(data[0])



	time.sleep(1)
	
	# except:
	# 	print("Exited code")
	# 	BT.close_connection()
	# 	break