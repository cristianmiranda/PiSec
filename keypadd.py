import time

import RPi.GPIO as GPIO

import Flask.alarmservice as AlarmService

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

MATRIX = [[1, 2, 3, 'A'],
          [4, 5, 6, 'B'],
          [7, 8, 9, 'C'],
          ["*", 0, "#", 'D']]

#ROW = [33, 31, 29, 32]
#COL = [12, 16, 18, 22]

ROW = [13, 6, 5, 12]
COL = [18, 23, 24, 25]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
number = ""

try:
    while (True):
        for j in range(4):
            GPIO.output(COL[j], 0)

            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    print MATRIX[i][j]
                    number = number + str(MATRIX[i][j])
                    print "String"
                    print number
                    while GPIO.input(ROW[i]) == 0:
                        time.sleep(0.2)
                        pass

            if len(number) == 4:
                status = AlarmService.get_status()
                if status == '1':
                    AlarmService.alarm_off(number)
                else:
                    AlarmService.alarm_on(number)
                time.sleep(0.5)
                number = ""
            GPIO.output(COL[j], 1)

except KeyboardInterrupt:
    print ("Quit")
    GPIO.cleanup()
