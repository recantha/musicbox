# Raspberry Pi Music Box
# Code by Michael Horne
# Some code based on code written by Pimoroni - https://github.com/pimoroni/Piano-HAT

from gpiozero import Button, MCP3008, LED
import glob
import os
import re
import time
import fluidsynth

# Start up the Synth and load the sound font
fs = fluidsynth.Synth()
fs.start(driver='alsa')
sfid = fs.sfload("soundfonts/JR_church.SF2")
fs.program_select(0, sfid, 0, 0)

# Set some globals
note_multiplier = 1
volume = 60

# Set-up buttons for reset and shutdown
button_reset = Button(23)
button_shutdown = Button(5)

# Set-up buttons for keyboard input
thumb_bottom = Button(13)
thumb_top = Button(6)
thumb_right = Button(12)
index_finger = Button(16)
middle_finger = Button(19)
ring_finger = Button(20)
pinky_finger = Button(21)

# Test procedure for the keyboard buttons
test_buttons = 0
if test_buttons:
	while True:
		print("Tbot:{}/Ttop:{}/Trih:{}/Idx:{}/Mid:{}/Rng:{}/Pnk:{}".format(thumb_bottom.value, thumb_top.value, thumb_right.value, index_finger.value, middle_finger.value, ring_finger.value, pinky_finger.value))
		time.sleep(0.2)


# Define potentiometers
pot0 = MCP3008(channel=2)
pot1 = MCP3008(channel=1)
pot2 = MCP3008(channel=0)

# Turn the light on
led_purple = LED(24)
led_purple.on()

def play_note(note):
	global fs
	fs.noteon(0, note, 60)

def octave_up():
    global octave
    if octave < octaves:
        octave += 1
        print('Selected Octave: {}'.format(octave))

def octave_down():
    global octave
    if octave > 0:
        octave -= 1
        print('Selected Octave: {}'.format(octave))

def shutdown():
	global main_loop_stopped, stop_main_loop

	print("Shutdown requested")

	stop_main_loop = 1
	while not main_loop_stopped:
		pass

	print("Shutting down the Pi")
	for chan in [7,6,5,4,3,2,1]:
		play_note(chan*3)
		time.sleep(0.2)
	os.system("sudo halt")
	exit("Shutdown")

def reset():
	global main_loop_stopped, stop_main_loop

	print("Reset requested")

	stop_main_loop = 1
	while not main_loop_stopped:
		pass

	print("Resetting the Pi")
	for chan in [7,6,5,4,3,2,1,2,3,4,5,6,7]:
		play_note(chan*3)
		time.sleep(0.1)
	os.system("sudo reboot")
	exit("Rebooting")

def startup():
	print("RASPBERRY PI MUSIC BOX")
	fs.noteon(0, 60, 60)
	fs.noteon(0, 50, 60)
	time.sleep(0.5)
	fs.noteoff(0, 60)
	fs.noteoff(0, 50)

thumb_bottom_note = 54
thumb_right_note = 56
thumb_top_note = 58
index_finger_note = 60
middle_finger_note = 62
ring_finger_note = 64
pinky_finger_note = 66

def thumb_top_start():
	fs.noteon(0, thumb_top_note, volume)

def thumb_top_stop():
	fs.noteoff(0, thumb_top_note)

def thumb_right_start():
	fs.noteon(0, thumb_right_note, volume)

def thumb_right_stop():
	fs.noteoff(0, thumb_right_note)

def thumb_bottom_start():
	fs.noteon(0, thumb_bottom_note, volume)

def thumb_bottom_stop():
	fs.noteoff(0, thumb_bottom_note)

def index_finger_start():
	fs.noteon(0, index_finger_note, volume)

def index_finger_stop():
	fs.noteoff(0, index_finger_note)

def middle_finger_start():
	fs.noteon(0, middle_finger_note, volume)

def middle_finger_stop():
	fs.noteoff(0, middle_finger_note)

def ring_finger_start():
	fs.noteon(0, ring_finger_note, volume)

def ring_finger_stop():
	fs.noteoff(0, ring_finger_note)

def pinky_finger_start():
	fs.noteon(0, pinky_finger_note, volume)

def pinky_finger_stop():
	fs.noteoff(0, pinky_finger_note)

# Play a tone so we know that we've started
startup()

# Set-up main loop watchers
main_loop_stopped = 0
stop_main_loop = 0

print("Initialising rear buttons")
button_reset.when_pressed = reset
button_shutdown.when_pressed = shutdown

# Assign actions to when_pressed for each button
thumb_bottom.when_pressed = thumb_bottom_start
thumb_bottom.when_released = thumb_bottom_stop
thumb_right.when_pressed = thumb_right_start
thumb_right.when_released = thumb_right_stop
thumb_top.when_pressed = thumb_top_start
thumb_top.when_released = thumb_top_stop
index_finger.when_pressed = index_finger_start
index_finger.when_released = index_finger_stop
middle_finger.when_pressed = middle_finger_start
middle_finger.when_released = middle_finger_stop
ring_finger.when_pressed = ring_finger_start
ring_finger.when_released = ring_finger_stop
pinky_finger.when_pressed = pinky_finger_start
pinky_finger.when_released = pinky_finger_stop

print("Starting main loop")

# Main loop
while not stop_main_loop:
	pass

main_loop_stopped = 1
while True:
	pass
