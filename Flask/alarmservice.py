from flask import Flask, send_file

import time
import os
import subprocess
import RPi.GPIO as GPIO
#import time as GPIO

red_PIN = 16
buzz_PIN = 26

#MAIN_PATH = "/home/pi/PiSec"
MAIN_PATH = "/Users/cristianmiranda/Documents/Work/Workspace_UNLaM/PiSec"
PASSWORD_PATH = MAIN_PATH + "/Flask/password"
STATUS_PATH = MAIN_PATH + "/Flask/status"

app = Flask(__name__)

@app.route('/alarm/password/<number>')
def set_password(number):
	with open(PASSWORD_PATH,"wb") as fo:
		fo.write(number)
        return 'Clave guardada!'

@app.route('/alarm/password')
def get_password():
	with open(PASSWORD_PATH,"rb") as fo:
		return fo.read()

@app.route('/alarm/status')
def get_status():
    with open(STATUS_PATH, "rb") as fo:
        return fo.read()

@app.route('/alarm/on/<number>')
def alarm_on(number):
    result = 'Clave incorrecta!'
    password = get_password()
    if number == password:
        result = 'Alarma activada'
        with open(STATUS_PATH, "wb") as fo:
            fo.write('1')
    return result

@app.route('/alarm/off/<number>')
def alarm_off(number):
    result = 'Clave incorrecta!'
    password = get_password()
    if number == password:
        result = 'Alarma desactivada'
        with open(STATUS_PATH, "wb") as fo:
            fo.write('0')
    return result

@app.route('/alarm/picture')
def take_picture():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz_PIN, GPIO.OUT)
    GPIO.setup(red_PIN, GPIO.OUT)
    grab_cam = subprocess.Popen("sudo fswebcam -r 640x480 -S 10 -d /dev/video0 -q " + MAIN_PATH + "/Alarm/pictures/manual/%m-%d-%y-%H%M%S.jpg", shell=True)
    grab_cam.wait()
    GPIO.output(red_PIN, True)
    GPIO.output(buzz_PIN, True)
    time.sleep(0.3)
    GPIO.output(red_PIN, False)
    GPIO.output(buzz_PIN, False)
    return get_manual_picture()

@app.route('/alarm/picture/manual')
def get_manual_picture():
    picture = os.popen("ls -Art " + MAIN_PATH + "/Alarm/pictures/manual | tail -n 1")
    filename = MAIN_PATH + '/Alarm/pictures/' + picture.read().rstrip('\n')
    return send_file(filename, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
