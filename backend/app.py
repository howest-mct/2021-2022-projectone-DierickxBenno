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
import os

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
scherm = LCDcontrol(17, 5, 6, 13, 19, 26, 21, 20, 27, 22)
scherm.init_screen([1,1,0], [1,0,0])
scherm.show_ip()

channel = "hci0"
mac = "78:21:84:7D:85:BE"



def connect_to_esp32():
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
            pass
    return DogBit

DogBit = connect_to_esp32()



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
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/stappen')
def stappen():
    pass


# socketio
@socketio.on('connect')
def initial_connection():
    print('A new client connected')
    #meestrecente data doorsturen
    most_recent_data = DataRepository.get_most_recent_data() #most recent data
    socketio.emit('B2F_meest_recente_data', {'data': most_recent_data}, broadcast=True)
    #totaal aantal stappen, vandaag doorsturen
    total_steps = DataRepository.get_total_steps()
    socketio.emit('B2F_stap', {'stap': total_steps})
    #historiek
    historiek = DataRepository.get_historiek()
    # print(historiek)
    socketio.emit('B2F_historiek', {"historiek": historiek})

    hue = DataRepository.get_hue()
    socketio.emit('B2F_curr_hue', {"hue": hue})

@socketio.on('F2B_set_color')
def send_hue(jsonObject):
    data = DataRepository.set_hue(jsonObject['hue'])
    DogBit.sendBT(f"hue: {jsonObject['hue']}")
    socketio.emit('B2F_curr_hue', {"hue": jsonObject['hue']})

@socketio.on('F2B_poweroff')
def poweroff(par):
    return os.system("sudo poweroff")

def get_data():
    while True:
        # receive
        data = (DogBit.recv())
        if data != None:
            if 'temperatuur' in data:
                print('temp measured')
                temperatuur = float(data[-5:])
                DataRepository.insert_data(temperatuur, 7)
                socketio.emit('B2F_temperatuur', {'temperatuur': temperatuur})
            
            elif 'stappen +' in data:
                print('step taken')
                stappen = int(data[9:])
                DataRepository.insert_data(stappen, 2)
                total_steps = DataRepository.get_total_steps()
                socketio.emit('B2F_stap', {'stap': total_steps})

            elif '$GP' in data:
                gps_data = PA1616s.getInfo(data)
                print('GPS data received')
                
                if gps_data is not None:
                    if gps_data["data-id"] == "$GPGGA" or gps_data["data-id"] == "$GPRMC":
                        longi = gps_data["longitude"]
                        lat = gps_data["latitude"]
                        DataRepository.add_location(longi, lat)

                        if gps_data["data-id"] == "$GPRMC":
                            if gps_data["validity"] == "A": # A betekent valid
                                snelheid = gps_data["speed"]
                                DataRepository.insert_data(snelheid, 1)



                    socketio.emit('B2F_GPS', {'GPS': gps_data})

            elif 'LI' in data:
                print("nieuwe licht intensiteit gemeten")
                licht_intensiteit = float(data[3:])
                DataRepository.insert_data(licht_intensiteit, 6)
            
            elif 'pulse' in data:
                pulse = float(data[7:])
                DataRepository.insert_data(pulse, 5)

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