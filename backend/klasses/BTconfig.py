import os

class BTconfig:
	def __init__(self, p_channel, p_mac):
		self.mac_adres = p_mac
		self.channel = p_channel
	
	def open_connection(self):
		cmd = f"sudo rfcomm connect {self.channel} {self.mac_adres} &"
		print(os.system(cmd))
	
	def close_connection(self):
		cmd = f"sudo rfcomm release {self.channel} {self.mac_adres} &"
		os.system(cmd)
		print("disconnected")

		