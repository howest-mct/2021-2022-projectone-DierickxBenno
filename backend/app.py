import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
print("zit just")
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from klasses.SerCom import SerCom
from klasses.BTconfig import BTconfig
from klasses.PA1616s import PA1616s

from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

channel = "hci0"
mac = "78:21:84:7D:85:BE"

BT = BTconfig(channel, mac)
BT.open_connection()

time.sleep(1)
DogBit = SerCom("rfcomm0")

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


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    most_recent_data = DataRepository.get_most_recent_data() #most recent data

    socketio.emit('B2F_meest_recente_data', {'data': most_recent_data}, broadcast=True)


# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     # Ophalen van de data
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

#     # Stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)

#     # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)

#     # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#     if lamp_id == '3':
#         print(f"TV kamer moet switchen naar {new_status} !")
#         GPIO.output(ledPin, new_status)


def get_data():
    while True:
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
                socketio.emit('B2F_stap', {'stap': 1})

            elif '$GP' in data:
                gps_data = PA1616s.getInfo(data)
                print('GPS data received')

                if gps_data is not None:
                    if gps_data["data-id"] == "$GPGGA" or gps_data["data-id"] == "$GPRMC":
                        longi = gps_data["longitude"]/100
                        lat = gps_data["latitude"]/100
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


def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')       
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()

if __name__ == '__main__':
    try:
        start_thread()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')

    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')

    finally:
        GPIO.cleanup()