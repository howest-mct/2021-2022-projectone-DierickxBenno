from RPi import GPIO
import time
#om linux commands uit te voeren
from subprocess import check_output

class LCDcontrol:
	def __init__(self, p_dp0, p_dp1, p_dp2, p_dp3, p_dp4, p_dp5, p_dp6, p_dp7, p_rs_pin, p_enable_pin):
		self.dp0 =  p_dp0
		self.dp1 =  p_dp1
		self.dp2 =  p_dp2
		self.dp3 =  p_dp3
		self.dp4 =  p_dp4
		self.dp5 =  p_dp5
		self.dp6 =  p_dp6	
		self.dp7 =  p_dp7	
		self.rs_pin = p_rs_pin
		self.enable_pin = p_enable_pin

		self.message = ''

		self.output_vals = [self.dp0, self.dp1, self.dp2, self.dp3, self.dp4, self.dp5, self.dp6, self.dp7, self.rs_pin, self.enable_pin]
		self.datapins = [self.dp0, self.dp1, self.dp2, self.dp3, self.dp4, self.dp5, self.dp6, self.dp7]

		#setup GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.output_vals, GPIO.OUT)

	def set_data_bits(self, p_databits):
		for i in range(8):
			GPIO.output(self.datapins[i], p_databits >> i & 1)

	def send_instruction(self, value):
		print("sending instruction ...")
		GPIO.output(self.rs_pin, 0)
		GPIO.output(self.enable_pin, 1)
		self.set_data_bits(value)
		time.sleep(0.01)
		GPIO.output(self.enable_pin, 0)

	def send_character(self, value):
		if type(value) is str():
			value = bin(ord(value))

		GPIO.output(self.rs_pin, 1)
		GPIO.output(self.enable_pin, 1)
		time.sleep(0.01)
		self.set_data_bits(value)	
		time.sleep(0.01)
		GPIO.output(self.enable_pin, 0)

	def set_interface(self, p_dl, p_lines, p_res):
		print("setting interface (x lines, resolution, data length)...")
		byte = 0b00100000
		byte |= p_dl <<4
		byte |= p_lines <<3
		byte |= p_res <<2
		
		GPIO.output(self.enable_pin, 1)
		self.send_instruction(byte)
		time.sleep(0.01)
		GPIO.output(self.enable_pin, 0)
	
	def clear_display(self):
		print("clearing display ...")
		#clear display
		GPIO.output(self.enable_pin, 1)
		self.send_instruction(0b1)
		GPIO.output(self.enable_pin, 0)
		
		#set cursor home
		print("setting cursor home ...")
		GPIO.output(self.enable_pin, 1)
		time.sleep(0.01)
		self.send_instruction(0b10)
		time.sleep(0.01)
		GPIO.output(self.enable_pin, 0)

	def display_settings(self, p_blink, p_cursor, p_display):
		print("setting screen settings (blink, cursor, display on/off)...")
		byte = 0b00001000
		byte |= p_display <<2
		byte |= p_cursor <<1
		byte |= p_blink
	
		GPIO.output(self.enable_pin, 1)
		time.sleep(0.01)
		self.send_instruction(byte)
		time.sleep(0.01)
		GPIO.output(self.enable_pin, 0)

	def init_screen(self, p_pars_interface, p_pars_display):
		print("initialise strated ...")
		self.set_interface(p_pars_interface[0], p_pars_interface[1], p_pars_interface[2])
		self.display_settings(p_pars_display[0], p_pars_display[1], p_pars_display[2])
		self.clear_display()

	def send_message(self, p_autoNewline = False, p_message=None):
		if p_message is None:
			self.message = input("wat wilt u zeggen?>> ")
		else:
			self.message = p_message

		teller = 0
		for letter in self.message:
			self.send_character(ord(letter))
			teller +=1
			if (teller == 16 and (p_autoNewline)):
				self.send_instruction(0b1<<7|0x40)
				teller=0

	def kies_cursor_opties(self, p_onoff=1, p_blink=1, p_home=None, p_position=None):
		#on/off
		self.send_instruction((0b00001100|(p_onoff<<1))|p_blink)
		#home
		if p_home is not None:
			self.send_instruction(0b10&(p_home<<1))
		#position
		if p_position is not None:
			self.send_instruction(0b1<<7|p_position)

	def show_ip(self):
		ips = str(check_output(['hostname', '-I']))
		first_space = ips.find(' ')
		self.kies_cursor_opties(p_position=0x00)
		self.send_message(p_message = ips[2:first_space])
		self.kies_cursor_opties(p_position=0x40)
		str_after = ips[first_space+1:]
		self.send_message(p_message = str_after[:str_after.find(' ')])
		print(f"{str_after[:str_after.find(' ')]}\n{ips[2:first_space]}")
