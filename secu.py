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
GPIO.output(RED_LED, GPIO.HIGH) #Red LED set to off
GPIO.output(GREEN_LED, GPIO.HIGH) #Green LED set to on

input_value = RPIO.input(<input_port_number>)

'''
#Imports
import time
import subprocess
import os
import _thread as thread
import smtplib
import getpass

#Network Email configuration
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

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

wire = [18, 22, 29, 31, 33, 38]

#Path to the Safe box folder
path = "~/git/secu/Safe\ Box"

#Variable for inter-thread communication
disarmed = 0
time_left = 120 #seconds

def auto_destroy():
	correct_wires = [18, 22, 38]

	print("Red LED ON")
	#GPIO.output(RED_LED, GPIO.LOW)
	disconnected = 0
	wrong_wire_counter = 0
	correct_wire_counter = 0
	global time_left

	thread.start_new_thread(countdown, ())
	thread.start_new_thread(buzzer_led, ())
	while(disconnected == 0 and time_left > 0):
		correct = 1
		#print("Outer correct = 1")

		for port in wire:
			#aux = RPIO.input(port)
			print(str(port) + " wire is ON(0) or OFF(1)?")
			aux = int(input())
			if(aux == 1):	#'''GPIO.HIGH'''
				correct = 0
				#print("correct = 0")
				
				for pin in correct_wires:
					if(port == pin):
						correct_wires.remove(port)
						#print("port == pin")
						correct = 1
						if(correct_wire_counter < 2):
							correct_wire_counter += 1
						else:
							#GPIO.output(RED_LED, GPIO.HIGH) #RED_LED is turned off.
							#GPIO.output(GREEN_LED, GPIO.LOW) #GREEN_LED is turned on.
							print("Bomb successfuly defused!")

							# correct = 0
							disconnected = 1
							break
						#print("correct = 1")
				if(correct == 0):
					if(wrong_wire_counter < 2):
						wrong_wire_counter += 1
					else:
						print("The bomb has exploded!")
						#exploded()
						disconnected = 1
						break
	if(time_left == 0):
		print("Time is up, the bomb has exploded!")
		time.sleep(0.3)
		#os.system("sudo shutdown now")

'''Open ~/.bash_aliases for editing.

nano ~/.bash_aliases
Insert the following line at the end of the file:

alias shutdown='sudo shutdown now' 
Finally, load the changes to the .bash_aliases file...

source ~/.bash_aliases
Try it out!

shutdown'''

		#exploded()
#	thread.start_new_thread(disarmed, ())

def countdown():
	print("The countdown has started!")
	time.sleep(120)
	global time_left
	time_left = 0

def buzzer_led():
	delay = 23
	global time_left
	while(time_left > 0):
		#GPIO.output(RED_LED, GPIO.LOW)
		#GPIO.output(BUZZER, GPIO.LOW)
		print("Red LED is ON")
		print("Buzzer is ON")
		time.sleep(0.1)
		#GPIO.output(RED_LED, GPIO.HIGH)
		#GPIO.output(BUZZER, GPIO.HIGH)
		print("Red LED is OFF")
		print("Buzzer is OFF")
		time.sleep(delay)
		delay = delay*(4/5)

def folder_unlocked():
	#GPIO.output(GREEN_LED, GPIO.LOW) #GREEN_LED is turned on.
	os.system("rm -rf " + path)
	os.system("mkdir " + path)
	os.system("cd " + path)
	#os.system("echo $(date +%s) > " + path + "/access_time.txt")
	os.system("cp epoch_time " + path)
	os.system("cd Safe\ Box && ./epoch_time")
	access_time = os.popen("date +%s").read()
	# print("Access Time: " + str(access_time))
	#Try to send it to an email address.
	
	print("""
Enter your Gmail and password in order to inform the Security 
Manager of your access to the folder.""")
	
	email = input("\nEmail: ")
	email_password = getpass.getpass()
	#email_password = input("Input you password: ")
	#print("\nEmail: " + str(email) + " and Password: " + str(email_password))

	server.login(email, email_password)
	access_time = str(access_time)
	access_time = access_time.replace("\n", "")
	access_time += "."
	email_message = "Dear Security Manager,\n\nI hereby inform that I have accessed the Safe Box folder in the following Epoch time: " + access_time + "\n\nBest Regards,\n" + str(email)
	#print(email_message)
	server.sendmail(email, "hebertonbarros@gmail.com", email_message)
	server.sendmail(email, "gersinho9@gmail.com", email_message)


os.system("clear")
print("""Hello! Welcome to Secu, your company's security system.
Enter the password in order to unlock the Safe Box folder.
""")

password = 'a'#"ilovecomputerarchitecture"

answer = getpass.getpass()
print("")

if(answer == password):
	print("Folder successfuly unlocked!")
	folder_unlocked()

else:
	print("Wrong password, try again.\n")
	answer = getpass.getpass()
	print("")

	if(answer == password):
		print("Folder successfuly unlocked!")
		folder_unlocked()

	else:
		print("Wrong again, this is your last chance.\n")
		answer = getpass.getpass()
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
		disarmed = 0
		auto_destroy()