from flask import Flask, send_file

import time
import os
import subprocess
import RPi.GPIO as GPIO

# import time as GPIO

red_PIN = 16
green_PIN = 27
buzz_PIN = 26

MAIN_PATH = "/home/pi/PiSec"
# MAIN_PATH = "/Users/cristianmiranda/Documents/Work/Workspace_UNLaM/PiSec"
PASSWORD_PATH = MAIN_PATH + "/Flask/password"
STATUS_PATH = MAIN_PATH + "/Flask/status"

app = Flask(__name__)

'''
    Password management
'''


@app.route('/alarm/password/<number>')
def set_password(number):
    with open(PASSWORD_PATH, "wb") as fo:
        fo.write(number)
    return 'Clave guardada!'


@app.route('/alarm/password')
def get_password():
    with open(PASSWORD_PATH, "rb") as fo:
        return fo.read()


'''
    Alarm status management
'''


@app.route('/alarm/status')
def get_status():
    with open(STATUS_PATH, "rb") as fo:
        return fo.read()


@app.route('/alarm/on/<number>')
def alarm_on(number):
    return alarm_on_off('on', number)


@app.route('/alarm/off/<number>')
def alarm_off(number):
    return alarm_on_off('off', number)


def alarm_on_off(mode, number):
    result = 'Clave incorrecta!'
    password = get_password()
    if number == password:
        with open(STATUS_PATH, "wb") as fo:
            if mode == 'on':
                fo.write('1')
                result = 'Alarma activada'
                GPIO.output(buzz_PIN, True)
                GPIO.output(green_PIN, False)
                GPIO.output(red_PIN, True)
                time.sleep(0.5)
                GPIO.output(buzz_PIN, False)
                GPIO.output(red_PIN, False)
                time.sleep(0.5)
                GPIO.output(red_PIN, True)
                time.sleep(0.5)
                GPIO.output(red_PIN, False)
            else:
                fo.write('0')
                result = 'Alarma desactivada'
                GPIO.output(green_PIN, True)
                GPIO.output(red_PIN, False)
    return result

'''
    Sacar fotos
'''


@app.route('/alarm/picture/manual/take')
def take_picture_manual():
    return take_picture('manual')


@app.route('/alarm/picture/auto/take')
def take_picture_auto():
    return take_picture('auto')


def take_picture(mode):
    grab_cam = subprocess.Popen(
        "sudo fswebcam -r 640x480 -S 20 -d /dev/video0 -q " + MAIN_PATH + "/Alarm/pictures/" + mode + "/%m-%d-%y-%H%M%S.jpg",
        shell=True)
    grab_cam.wait()
    GPIO.output(red_PIN, True)
    GPIO.output(buzz_PIN, True)
    time.sleep(0.3)
    GPIO.output(red_PIN, False)
    GPIO.output(buzz_PIN, False)
    return 'Foto tomada!'


'''
    Obtener fotos
'''


@app.route('/alarm/picture/manual')
def get_manual_picture():
    return get_picture('manual')


@app.route('/alarm/picture/auto')
def get_auto_picture():
    return get_picture('auto')


def get_picture(mode):
    picture = os.popen("ls -Art " + MAIN_PATH + "/Alarm/pictures/" + mode + " | tail -n 1")
    filename = MAIN_PATH + '/Alarm/pictures/' + mode + '/' + picture.read().rstrip('\n')
    return send_file(filename, mimetype='image/gif')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz_PIN, GPIO.OUT)
    GPIO.setup(red_PIN, GPIO.OUT)
    GPIO.setup(green_PIN, GPIO.OUT)
    app.run(debug=True, host='0.0.0.0')
