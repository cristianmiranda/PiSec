import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BOARD)
 
MATRIX = [	[1,2,3, 'A'],
	    	[4,5,6, 'B'],
		[7,8,9, 'C'],
		["*",0,"#", 'D'] ]

ROW = [33,31,29,32]
COL = [12,16,18,22]

for j in range(4):
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)

for i in range(4):
	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
number = ""

try:
	while(True):
			for j in range(4):
				GPIO.output(COL[j], 0)
				
				for i in range(4):
					if GPIO.input(ROW[i]) == 0:
						print MATRIX[i][j]
                                        	number = number + str(MATRIX[i][j])
                                        	print "String"
                                        	print number
						while (GPIO.input(ROW[i]) == 0):
							time.sleep(0.2)
							pass

                                if len(number) == 4: 
					#mat_num = subprocess.Popen("links 10.0.0.109:5000/teclado/" +number, shell=True)
                                        mat_num = subprocess.Popen("links 192.168.1.73:5000/teclado/" +number, shell=True)
					#mat_num = subprocess.Popen("links 10.0.0.109:5000/hello/eze", shell=True)
                                        time.sleep(0.5)
					mat_num.kill()
					number = ""
				GPIO.output(COL[j], 1)
				
except KeyboardInterrupt:
        print ("Quit")
	GPIO.cleanup()
