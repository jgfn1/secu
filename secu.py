'''

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#GPIO Ports Setup
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(WIRES_VCC, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.setup(WIRE1, GPIO.IN)
GPIO.setup(WIRE2, GPIO.IN)
GPIO.setup(WIRE3, GPIO.IN)
GPIO.setup(WIRE4, GPIO.IN)
GPIO.setup(WIRE5, GPIO.IN)
GPIO.setup(WIRE6, GPIO.IN)

#I/O samples
GPIO.output(RED_LED, GPIO.HIGH)
GPIO.output(GREEN_LED, GPIO.HIGH)

input_value = RPIO.input(<input_port_number>)

'''
#Imports
import time
import os
import _thread as thread

#GPIO Ports Numbers
RED_LED = 7 #Change the LED wire to GPIO4
BLUE_LED = 11
BUZZER = 40

WIRES_VCC = 13 #GPIO27
WIRE1 = 18	#GPIO24
WIRE2 = 22	#GPIO25
WIRE3 = 29	#GPIO5	
WIRE4 = 31	#GPIO6 
WIRE5 = 33	#GPIO13
WIRE6 = 38	#GPIO20

#Path to the Safe box folder
path = "~/git/Safe\ Box"

#Variable for inter-thread communication

def auto_destroy():
	while(1):
		print("Red LED ON")
	#GPIO.output(RED_LED, GPIO.HIGH)

def folder_unlocked():
	os.system("cd " + path)

os.system("clear")
print("""Hello! Welcome to Secu, your company's security system.
Enter the password in order to unlock the Safe Box folder.
""")

password = "ilovecomputerarchitecture"

answer = input("Password: ")
print("")

if(answer == password):
	print("Folder successfuly unlocked!")

else:
	print("Wrong combination, try again.\n")
	answer = input("Password: ")
	print("")

	if(answer == password):
		print("Folder successfuly unlocked!")
		folder_unlocked()

	else:
		print("""
- - - RED ALERT!!! - - -

- - - INTRUDER DETECTED - - -

Defuse the bomb or the computer will auto destroy!
		""")

		thread.start_new_thread(auto_destroy, ())
while(1):
	print("Main thread")