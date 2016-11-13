import time

import RPi.GPIO as GPIO
from gpiozero import MotionSensor

import Flask.alarmservice as AlarmService

# Variables
MAIN_PATH = "/home/pi/PiSec"

# PIN
red_PIN = 16
pir = MotionSensor(17)
buzz_PIN = 26
green_PIN = 27

already_took = 0

def check_motion():
    if pir.motion_detected and already_took == 0:
        print("Motion detected!")
        print("Taking picture!")
        AlarmService.take_picture_auto()
        already_took = 1
        print("Done!")
    else:
        if not pir.motion_detected:
            already_took = 0


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz_PIN, GPIO.OUT)
    ## Los leds se usan de la siguiente forma:
    ## - Verde: alarma desactivada
    ## - Rojo: movimiento detectado
    ## - Apagados: alarma encendida

    GPIO.setup(red_PIN, GPIO.OUT)
    GPIO.setup(green_PIN, GPIO.OUT)

    print ("Iniciando PiSec...")
    print ("==================")
    password = AlarmService.get_password()
    AlarmService.alarm_off(password)

    # Verifica la excepcion de teclado para poder salir.
    try:
        while True:
            time.sleep(0.5)
            status = AlarmService.get_status()
            if status == '1':
                check_motion()

    except KeyboardInterrupt:
        print ("Quit")
