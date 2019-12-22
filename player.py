#Import Raspberry Pi GPIO library
import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import sys

#Start by clearing everything that may be left over from a wrong shutdown
command = subprocess.Popen(["pidof", "mpv"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
stdout, stderr = command.communicate()
if stdout.decode('UTF-8') != '':
	subprocess.call(["pkill", "mpv"])
	GPIO.output(music_playing_pin,GPIO.LOW)

#Use physical pin numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Inputs
start_stop_pin = 10

#Outputs
music_playing_pin = 12
ready_to_start_led = 11
GPIO.setup(music_playing_pin,GPIO.OUT)

GPIO.setup(ready_to_start_led,GPIO.OUT)
GPIO.output(ready_to_start_led,GPIO.HIGH)

#Xmas playlist dates
today = datetime.date.today()
#today = (t.month, t.day)
xmas_from = datetime.date(today.year, 11, 30)
#xmas_from = (12, 1)
xmas_to = datetime.date(today.year + 1, 1, 6)
#xmas_to = (1, 6)
print('Today is ', today.year,'/',today.month,'/',today.day)
print('Xmas from', xmas_from.year,'/',xmas_from.month,'/',xmas_from.day)
print('Xmas to', xmas_to.year,'/',xmas_to.month,'/',xmas_to.day)

def start_stop_button_callback(channel):
	time.sleep(0.005)
	# only deal with valid edges
	if GPIO.input(start_stop_pin) == 1:
		#check if there are mpv instances running
		command = subprocess.Popen(["pidof", "mpv"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		stdout, stderr = command.communicate()
		#print(stderr)
		if stdout.decode('UTF-8') == '':
			#if no mpv instance, start one
			if xmas_from < today < xmas_to:
				print('On xmas playlist')
				subprocess.Popen(["mpv", "/mnt/mydisk/xmas", "--no-audio-display", "--shuffle", "--gapless-audio", "--loop-playlist"])
			else:
				print('On regular playlist')
				subprocess.Popen(["mpv", "/mnt/mydisk/Playlist", "--no-audio-display", "--shuffle", "--gapless-audio", "--loop-playlist"])
			#light up the LED
			GPIO.output(music_playing_pin,GPIO.HIGH)
		else:
			#if there is an mpv instance, stop it:
			subprocess.call(["pkill", "mpv"])
			GPIO.output(music_playing_pin,GPIO.LOW)

# Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(start_stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Attach event to the pin; setup event on pin 10, rising edge
GPIO.add_event_detect(start_stop_pin, GPIO.RISING, callback=start_stop_button_callback)

#keep the script running
while 1:
        time.sleep(.5)

GPIO.cleanup()