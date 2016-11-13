from gpiozero import MotionSensor
import subprocess
import datetime
import RPi.GPIO as GPIO
import time

#Definiciones
red_PIN = 16
pir = MotionSensor(17)
buzz_PIN = 26
#green_PIN = XX

#Seteos
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz_PIN, GPIO.OUT)
## Los leds se usan de la siguiente forma:
## - Verde: alarma desactivada
## - Rojo: movimiento detectado
## - Apagados: alarma encendida

GPIO.setup(red_PIN, GPIO.OUT)
#GPIO.setup(green_PIN, GPIO.OUT)

#Comienzo de PiSec
print ("PIR Module Test (CTRL+C to exit)")
time.sleep(2)
print ("Ready")
n = 0
status = 0 #El sistema inicia desactivado

#Verifica la excepcion de teclado para poder salir.
try:
        while True:
                with open("/home/pi/Desktop/PiSec/passpisec.txt", "r+") as fo:
                        fo.seek(0, 0)
                        pwPisec = fo.read(1)
                fo.closed
                with open("/home/pi/Desktop/Flask/password", "r+") as fo:
                        fo.seek(0, 0)
                        pwWebService = fo.read(1)
                fo.closed
                #Habría que borrar el archivo password para que no quede siempre igual.
                if pwPisec == pwWebService and status = 0: #Verifica si las passwords son iguales y que el sistema está activo.
                        status = 1
                        GPIO.output(green_PIN, False)
                        GPIO.output(red_PIN, True)
                        time.sleep(60)
                        GPIO.output(red_PIN, False)
                else: #El sistema está activo, se procederá a desactivarlo.
                        GPIO.output(green_PIN, True)


                if status == 1 and pir.motion_detected:
                        grab_cam = subprocess.Popen("sudo fswebcam -r 640x480 -S 10 -d /dev/video0 -q /home/pi/Desktop/Alarm/pictures/%m-%d-%y-%H%M%S.jpg", shell=True)
                        grab_cam.wait()
                        GPIO.output(red_PIN, True)
                        GPIO.output(buzz_PIN, True)
                        n = n + 1
                        print("Motion detected!")
                        print (n)
                        time.sleep(0.3)
                        GPIO.output(red_PIN, False)
                        GPIO.output(buzz_PIN, False)

except KeyboardInterrupt:
        print ("Quit")
