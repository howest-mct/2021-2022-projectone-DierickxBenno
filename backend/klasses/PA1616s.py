# test values
# gga = "$GPGGA,102121.000,5008.5979,N,00537.4055,E,1,07,1.20,415.8,M,47.6,M,,*6E"
# rmc = "$GPRMC,102121.000,A,5008.5979,N,00537.4055,E,0.28,324.54,260522,,,A*6A"
#
# should return at least (also check out: https://cdn-shop.adafruit.com/product-files/746/CD+PA1616S+Datasheet.v03.pdf ):
# Time: 10:21:22.000
# Date: 26/5/2022
# Fix: 1 quality: 1
# Location: 5008.5977N, 537.4054E
# Speed (knots): 0.20
# Angle: 324.54
# Altitude: 415.80
# Satellites: 7


class PA1616s:
	@staticmethod
	def cdf(p_date): #conver date format (ddmmyy to yyyymmdd)
		# print(p_date)
		dd = p_date[:2]
		mm = p_date[2:4]
		yy = p_date[4:6]
		return f"20{yy}-{mm}-{dd}"

	@staticmethod
	def seperate_data(p_msg):
		data_list = []
		index = p_msg.find(",")

		while index != -1:
			data_list.append(p_msg[:index])
			p_msg = p_msg[(index+1):]
			index = p_msg.find(",")
		
		else:
			data_list.append(p_msg)
			return data_list

	@staticmethod
	def ctf(p_time): #Convert_Time_Format, van hhmmss.ssss naar hh:mm:ss
		hh = p_time[:2]
		mm = p_time[2:4]
		ss = p_time[4:6]
		return f"{hh}:{mm}:{ss}"

	@staticmethod
	def getInfo(p_msg):
		#data opsplitsen
		data = PA1616s.seperate_data(p_msg)
		msg_id = data[0]

		# data verwerken op basis van id
		if "$GPGGA" == msg_id and len(data) >= 15:
				time = PA1616s.ctf(data[1])

				lat = data[2]
				lat_NS = data[3] # N or S

				longi = data[4]
				longi_EW = data[5] # E or W
				
				pfi = data[6] # 0: Fix not available, 1: GPS FIX, 2: diffrential GPS fix (pfi = position fix indicator)
				HDOP = data[7] # Horizontal Dilution of Precision
				alt = data[8] #altitude to sea level
				tot_data = {
					"data-id": data[0],
					"time": time,
					"latitude": lat,
					"longitude": longi,
					"altitude": alt,
					"fix": pfi,
					"Horizontal Dilution of Precision": HDOP,
				}
				return tot_data

		elif "$GPRMC" == msg_id and len(data)>=13:
			time = PA1616s.ctf(data[1])

			status = data[2] # A=data valid or V=data not valid

			lat = data[3]
			lat_NS = data[4] # N or S

			longi = data[5]
			longi_EW = data[6] # E or W
			
			speed = float(data[7])*1.852
			datum = PA1616s.cdf(data[9])
			mode = data[12][0]

			tot_data = {
				"data-id": data[0],
				"time": time,
				"validity": status,
				"latitude": lat,
				"longitude": longi,
				"speed": speed,
				"datum": datum,
				"mode": mode
			}
			# print(tot_data)
			return tot_data

		elif "$GPGSA" == msg_id and len(data)>=18:
			PDOP = data[7]
			tot_data = {"data-id": data[0],"PDOP": PDOP}
			return tot_data



