import serial
import os

class SerCom:
	def __init__(self, serport):
		self.serport = serport
		self.ser = serial.Serial(f'/dev/{serport}', 9600, timeout=1)
		self.ser.reset_input_buffer()
		
	def send(self, p_msg):
		p_msg += "\n"
		self.ser.write(p_msg.encode("utf8"))
	
	def sendBT(self, p_msg):
		cmd = f"echo '{p_msg}' > /dev/{self.serport}"
		os.system(cmd)

	def recv(self): #'/dev/ttyS0' bij TXRX arduino
		if self.ser.in_waiting > 0:
			line = self.ser.readline().decode('utf-8').rstrip()
			return line
		
