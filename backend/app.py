import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
# print(__name__, time.now())
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from klasses.SerCom import SerCom
from klasses.BTconfig import BTconfig
from klasses.PA1616s import PA1616s
from klasses.LCD import LCDcontrol

from selenium import webdriver
from datetime import datetime
import os

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
scherm = LCDcontrol(17, 5, 6, 13, 19, 26, 21, 20, 27, 22)
scherm.init_screen([1,1,0], [1,0,0])
scherm.show_ip()
scherm.kies_cursor_opties(0,0)

channel = "hci0"
mac = "78:21:84:7D:85:BE"

    

def connect_to_esp32():
    global DogBit
    print('connecting to BT...')
    BT = BTconfig(channel, mac)
    time.sleep(2)
    while 1:
        try:
            BT.open_connection()
            time.sleep(2)
            DogBit = SerCom("rfcomm0")
            break
            
        except:
            # print('.')
            pass
    # return DogBit

DogBit = None
status_led = 'start'
fix = 0


# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print("error: ", e)

# API ENDPOINTS
endpoint = '/api/v1/'
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."



@app.route(endpoint+'/historiek/day/', methods=['GET'])
def dag_historiek():
    data = DataRepository.get_historiek_day()
    data_to_send = []
    
    stappen = {}
    speed = {}
    temp = {}
    heartrate = {}
    print('sending data to client')
    for eenheid in data:
        e_id = eenheid['eenheidid']
        x = datetime.fromtimestamp(eenheid['x']/1000)
        x = x.strftime('%x %H')


        if (e_id == 1):
            if (x in speed.keys()):
                speed[x].append(float(eenheid['y']))

            elif (x not in speed.keys()): 
                speed[x] = [float(eenheid['y'])]

        
        elif (e_id == 2):
            if (x in stappen.keys()):
                stappen[x] += int(eenheid['y'])

            elif (x not in stappen.keys()): 
                stappen[x] = int(eenheid['y'])

        elif (e_id == 5):
            if (x in heartrate.keys()):
                heartrate[x].append(float(eenheid['y']))

            elif (x not in heartrate.keys()): 
                heartrate[x] = [float(eenheid['y'])]
        
        elif (e_id == 7):
            if (x in temp.keys()):
                temp[x].append(float(eenheid['y']))

            elif (x not in temp.keys()): 
                temp[x] = [float(eenheid['y'])]
    # making viable data
    print('...')
    for i in stappen:
        x = datetime.timestamp(datetime.strptime(i+':00:00', '%x %X'))*1000
        data_to_send.append({'eenheidid': 2, 'x':x, 'y': stappen[i]})   
    
    for i in temp:
        # print('temp', i)
        x = datetime.timestamp(datetime.strptime(i+':00:00', '%x %X'))*1000
        data_to_send.append({'eenheidid': 7, 'x':x, 'y': sum(temp[i])/len(temp[i])}) 

    for i in speed:
        x = datetime.timestamp(datetime.strptime(i+':00:00', '%x %X'))*1000
        data_to_send.append({'eenheidid': 1, 'x':x, 'y': sum(speed[i])/len(speed[i])})   
    
    for i in heartrate:
        x = datetime.timestamp(datetime.strptime(i+':00:00', '%x %X'))*1000
        data_to_send.append({'eenheidid': 1, 'x':x, 'y': sum(heartrate[i])/len(heartrate[i])})   
    
    print(jsonify(data_to_send))        

    print('data sent to client')
    return jsonify(data_to_send)

@app.route(endpoint+'/historiek/week/', methods=['GET'])
def week_historiek():
    data = DataRepository.get_historiek_week()
    data_to_send = []
    
    stappen = {}
    speed = {}
    temp = {}
    heartrate = {}
    print('sending data to client')
    for eenheid in data:
        e_id = eenheid['eenheidid']
        x = datetime.fromtimestamp(eenheid['x']/1000)
        x = x.strftime('%x')


        if (e_id == 1):
            if (x in speed.keys()):
                speed[x].append(float(eenheid['y']))

            elif (x not in speed.keys()): 
                speed[x] = [float(eenheid['y'])]

        
        elif (e_id == 2):
            if (x in stappen.keys()):
                stappen[x] += int(eenheid['y'])

            elif (x not in stappen.keys()): 
                stappen[x] = int(eenheid['y'])

        elif (e_id == 5):
            if (x in heartrate.keys()):
                heartrate[x].append(float(eenheid['y']))

            elif (x not in heartrate.keys()): 
                heartrate[x] = [float(eenheid['y'])]
        
        elif (e_id == 7):
            if (x in temp.keys()):
                temp[x].append(float(eenheid['y']))

            elif (x not in temp.keys()): 
                temp[x] = [float(eenheid['y'])]

    # making viable data
    print('...')
    for i in stappen:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 2, 'x':x, 'y': stappen[i]})   
    
    for i in temp:
        # print('temp', i)
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 7, 'x':x, 'y': sum(temp[i])/len(temp[i])}) 

    for i in speed:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 1, 'x':x, 'y': sum(speed[i])/len(speed[i])})   
    
    for i in heartrate:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 5, 'x':x, 'y': sum(heartrate[i])/len(heartrate[i])})   
    
    print(jsonify(data_to_send))        

    print('data sent to client')
    return jsonify(data_to_send)

@app.route(endpoint+'/historiek/month/', methods=['GET'])
def month_historiek():
    data = DataRepository.get_historiek_month()
    data_to_send = []
    
    stappen = {}
    speed = {}
    temp = {}
    heartrate = {}
    print('sending data to client')
    for eenheid in data:
        e_id = eenheid['eenheidid']
        x = datetime.fromtimestamp(eenheid['x']/1000)
        x = x.strftime('%x')


        if (e_id == 1):
            if (x in speed.keys()):
                speed[x].append(float(eenheid['y']))

            elif (x not in speed.keys()): 
                speed[x] = [float(eenheid['y'])]

        
        elif (e_id == 2):
            if (x in stappen.keys()):
                stappen[x] += int(eenheid['y'])

            elif (x not in stappen.keys()): 
                stappen[x] = int(eenheid['y'])

        elif (e_id == 5):
            if (x in heartrate.keys()):
                heartrate[x].append(float(eenheid['y']))

            elif (x not in heartrate.keys()): 
                heartrate[x] = [float(eenheid['y'])]
        
        elif (e_id == 7):
            if (x in temp.keys()):
                temp[x].append(float(eenheid['y']))

            elif (x not in temp.keys()): 
                temp[x] = [float(eenheid['y'])]
    # making viable data
    print('...')
    for i in stappen:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 2, 'x':x, 'y': stappen[i]})   
    
    for i in temp:
        # print('temp', i)
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 7, 'x':x, 'y': sum(temp[i])/len(temp[i])}) 

    for i in speed:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 1, 'x':x, 'y': sum(speed[i])/len(speed[i])})   
    
    for i in heartrate:
        x = datetime.timestamp(datetime.strptime(i, '%x'))*1000
        data_to_send.append({'eenheidid': 5, 'x':x, 'y': sum(heartrate[i])/len(heartrate[i])})   
    
    print((data_to_send))        

    print('data sent to client')
    return jsonify(data_to_send)

# socketio
@socketio.on('connect')
def initial_connection():
    print('A new client connected')
    #meestrecente data doorsturen
    most_recent_data = DataRepository.get_most_recent_data() #most recent data
    socketio.emit('B2F_meest_recente_data', {'data': most_recent_data}, broadcast=True)
    #totaal aantal stappen, vandaag doorsturen
    total_steps = DataRepository.get_total_steps()
    socketio.emit('B2F_stap', {'stap': total_steps}, broadcast=True)

    hue = DataRepository.get_hue()
    socketio.emit('B2F_curr_hue', {"hue": hue}, broadcast=True)

@socketio.on('F2B_set_color')
def send_hue(jsonObject):
    data = DataRepository.set_hue(jsonObject['hue'])
    print(jsonObject)
    if DogBit != None:
        DogBit.sendBT(f"hue: {jsonObject['hue']}")
        socketio.emit('B2F_curr_hue', {"hue": jsonObject['hue']}, broadcast=True)

@socketio.on('F2B_poweroff')
def poweroff(par):
    return os.system("sudo poweroff")

def get_data():
    global fix, DogBit
    connect_to_esp32()
    # DogBit = 

    while True:
        global status_led
        # receive
        data = (DogBit.recv())
        if data != None:
            if 'temperatuur' in data:
                print('temp measured')
                temperatuur = float(data[-5:])
                DataRepository.insert_data(temperatuur, 7)
                print(temperatuur)
                socketio.emit('B2F_temperatuur', {'temperatuur': temperatuur}, broadcast=True)
            
            elif 'stappen +' in data:
                print('step taken')
                stappen = int(data[9:])
                DataRepository.insert_data(stappen, 2)
                total_steps = DataRepository.get_total_steps()
                socketio.emit('B2F_stap', {'stap': total_steps}, broadcast=True)

            elif '$GP' in data:
                gps_data = PA1616s.getInfo(data)
                print('GPS data received')
                if gps_data is not None:
                    if gps_data["data-id"] == "$GPGGA" or gps_data["data-id"] == "$GPRMC":
                        longi = gps_data["longitude"]
                        lat = gps_data["latitude"]
                        if gps_data["data-id"] == '$GPGGA':
                            fix = gps_data['fix']
                        
                        if fix:
                            if (longi and lat):
                                DataRepository.add_location(longi, lat)


                        if gps_data["data-id"] == "$GPRMC" and fix == 1:
                            if gps_data["validity"] == "A": # A betekent valid
                                snelheid = gps_data["speed"]
                                DataRepository.insert_data(snelheid, 1)



                    socketio.emit('B2F_GPS', {'GPS': gps_data}, broadcast=True)

            elif 'LI' in data:
                licht_intensiteit = float(data[3:])
                DataRepository.insert_data(licht_intensiteit, 6)
                print(licht_intensiteit)    
            
            elif 'pulse' in data:
                pulse = float(data[7:])
                DataRepository.insert_data(pulse, 5)

            elif 'LEDSTATUS' in data:
                if ('OFF' in data and (status_led == 1 or status_led == 'start')):
                    socketio.emit("B2F_status_led", {"status": "status: off"}, broadcast=True)
                    status_led = 0
                    DataRepository.set_led_status_off()
                
                elif ('ON' in data and (status_led == 0 or status_led == 'start')):
                    socketio.emit("B2F_status_led", {"status": "status: on"}, broadcast=True)
                    status_led = 1   
                    DataRepository.set_led_status_on()


def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=get_data, args=(), daemon=True)
    thread.start()

if __name__ == '__main__':
    try:
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')

    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')

    finally:
        GPIO.cleanup()