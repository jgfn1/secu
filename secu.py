import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#GPIO Ports Numbers
RED_LED = 7 #Change the LED wire to GPIO4
GREEN_LED = 11
BUZZER = 40

WIRES_VCC = 15 #GPIO27

WIRE1 = 18	#GPIO24
WIRE2 = 22	#GPIO25
WIRE3 = 29	#GPIO5	
WIRE4 = 31	#GPIO6 
WIRE5 = 33	#GPIO13
WIRE6 = 38	#GPIO20

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

GPIO.output(RED_LED, GPIO.LOW)
GPIO.output(GREEN_LED, GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)
GPIO.output(WIRES_VCC, GPIO.HIGH)

#I/O samples
# GPIO.output(RED_LED, GPIO.HIGH) #Red LED set to off
# GPIO.output(GREEN_LED, GPIO.HIGH) #Green LED set to on

# input_value = RPIO.input(<input_port_number>)

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

invasionAttempt = "Dear security manager,\n\nI hereby inform you that someone has tried to hack into the sensetive files folder for the company. " + "The folder has been destroyed and everything has been stored to the security cloud. The system has also been successfully shut down for security purposes. Things are under control." + "\n\nBest Regards,\n" 

wire = [18, 22, 29, 31, 33, 38]

#Path to the Safe box folder
path = "/home/pi/Desktop/Assignment5/Safe\ Box"

time_left = 120 #seconds

def auto_destroy():
	correct_wires = [18, 22, 38]
	wire = [18, 22, 29, 31, 33, 38]
	
	disconnected = 0
	wrong_wire_counter = 0
	correct_wire_counter = 0
	global time_left

	thread.start_new_thread(countdown, ())
	thread.start_new_thread(buzzer_led, ())

	while(disconnected == 0 and time_left > 0):
		correct = 1
		# print("While")
		for port in wire:
			# print("External for")
			aux = GPIO.input(port)
			
			# print(str(port) + " wire is ON(1) or OFF(0)?")
			# aux = int(input())
			if(aux == GPIO.LOW):	#'''GPIO.HIGH'''
				correct = 0
				
				for pin in correct_wires:
					# print("Internal for")
					if(port == pin):
						correct_wires.remove(port)
						wire.remove(port)
						print("Correct wire removed!")
						correct = 1
						if(correct_wire_counter < 2):
							correct_wire_counter += 1
						else:

							GPIO.output(RED_LED, GPIO.LOW) #RED_LED is turned off.
							GPIO.output(GREEN_LED, GPIO.HIGH) #GREEN_LED is turned on.
							
							print("Bomb successfuly defused!")
							disconnected = 1
							break
            
				if(correct == 0):
					if(wrong_wire_counter < 2):
						print("Wrong wire " + str(wrong_wire_counter))
						wrong_wire_counter += 1
						wire.remove(port)
					else:
						print("The bomb has exploded!")
						time.sleep(2)

						os.system("rm -rf " + path)
						email = ""
						email_password = ""
						server.login(email, email_password)
						server.sendmail(email, "hebertonbarros@gmail.com", invasionAttempt)
						os.system("sudo shutdown now")
						
						disconnected = 1
						break
		time.sleep(0.2)

	if(time_left == 0):
		print("Time is up, the bomb has exploded!")		
		time.sleep(2)

def countdown():
	print("The countdown has started!")
	time.sleep(120)
	print("Time is over!")

	os.system("rm -rf " + path)
	email = ""
	email_password = ""
	server.login(email, email_password)
	server.sendmail(email, "hebertonbarros@gmail.com", invasionAttempt)
	os.system("sudo shutdown now")
	
	global time_left
	time_left = 0

def buzzer_led():
	delay = 21
	global time_left
	while(time_left > 0):

		GPIO.output(RED_LED, GPIO.HIGH)
		GPIO.output(BUZZER, GPIO.HIGH)
		
		# print("Red LED is ON")
		# print("Buzzer is ON")
		time.sleep(0.1)
		
		GPIO.output(RED_LED, GPIO.LOW)
		GPIO.output(BUZZER, GPIO.LOW)
		
		# print("Red LED is OFF")
		# print("Buzzer is OFF")
		time.sleep(delay)
		delay = delay*(4/5)

def folder_unlocked():

	GPIO.output(GREEN_LED, GPIO.HIGH) #GREEN_LED is turned on.

	os.system("cd " + path)
	#os.system("echo $(date +%s) > " + path + "/access_time.txt")
	os.system("cp epoch_time " + path)
	os.system("cd Safe\ Box && ./epoch_time")
	access_time = os.popen("date +%s").read()
	# print("Access Time: " + str(access_time))
	#Try to send it to an email address.
	
	print("""
Enter your Gmail and password in order to inform the head of security
of your access to the folder.""")
	
	email = input("\nEmail: ")
	email_password = getpass.getpass()
	#email_password = input("Input you password: ")
	#print("\nEmail: " + str(email) + " and Password: " + str(email_password))

	server.login(email, email_password)
	access_time = str(access_time)
	access_time = access_time.replace("\n", "")
	access_time += "."
	email_message = "Dear security manager,\n\nI hereby inform you that I have accessed the SECU folder at the following Epoch time: " + access_time + "\n\nBest Regards,\n" + str(email)
	#print(email_message)
	server.sendmail(email, "hebertonbarros@gmail.com", email_message)
	#You can enter any email you'd like to send a note to on here. 

os.system("clear")
print("""Welcome to Secu, your company's security system.
In order to unlock and get into this folder, you need to enter a password.
""")
os.system("rm -rf " + path)
os.system("mkdir " + path)

password = "ilovecomputerarchitecture"

answer = getpass.getpass()
print("")

if(answer == password):
	print("Folder successfully unlocked!")
	folder_unlocked()

else:
	print("Wrong password, try again.")
	print("Ps.: You only have two more attempts.")
	print("If you don't get the passward right, a bomb will be activated and all the files in this folder will be destroyed.")
	print("The way to defuse the bomb will be by removing a combination of wires.\n")
	answer = getpass.getpass()
	print("")

	if(answer == password):
		print("Folder successfully unlocked!")
		folder_unlocked()

	else:
		print("Wrong again, this is your last chance.\n")
		answer = getpass.getpass()
		print("")

		if(answer == password):
			print("Folder successfully unlocked!")
			folder_unlocked()

		else:
			print("""
--- RED ALERT!!! ---
--- INTRUDER DETECTED ---

Defuse the bomb by removing 3 correct wires, or else the folder
will auto destroy and the computer will be shut down!
			""")
		
		auto_destroy()
