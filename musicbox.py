# Raspberry Pi Music Box
# Code by Michael Horne
# Some code based on code written by Pimoroni - https://github.com/pimoroni/Piano-HAT

from __future__ import division
from gpiozero import Button, MCP3008, LED
import glob
import os
import re
import time
import fluidsynth

# Start up the Synth and load the sound font
fs = fluidsynth.Synth()
fs.start(driver='alsa')

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
	global stop_main_loop

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
	global stop_main_loop

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
	fs.noteon(0, 60, 100)
	fs.noteon(0, 50, 100)
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

last_note_thumb_top = thumb_top_note
def thumb_top_start():
	global last_note_thumb_top
	last_note_thumb_top = thumb_top_note+note_additor
	fs.noteon(0, last_note_thumb_top, volume)

def thumb_top_stop():
	fs.noteoff(0, last_note_thumb_top)

last_note_thumb_right = thumb_right_note
def thumb_right_start():
	global last_note_thumb_right
	last_note_thumb_right = thumb_right_note+note_additor
	fs.noteon(0, last_note_thumb_right, volume)

def thumb_right_stop():
	fs.noteoff(0, last_note_thumb_right)

last_note_thumb_bottom = thumb_bottom_note
def thumb_bottom_start():
	global last_note_thumb_bottom
	last_note_thumb_bottom = thumb_bottom_note+note_additor
	fs.noteon(0, last_note_thumb_bottom, volume)

def thumb_bottom_stop():
	fs.noteoff(0, last_note_thumb_bottom)

last_note_index_finger = index_finger_note
def index_finger_start():
	global last_note_index_finger
	last_note_index_finger = index_finger_note+note_additor
	fs.noteon(0, last_note_index_finger, volume)

def index_finger_stop():
	fs.noteoff(0, last_note_index_finger)

last_note_middle_finger = middle_finger_note
def middle_finger_start():
	global last_note_middle_finger
	last_note_middle_finger = middle_finger_note+note_additor
	fs.noteon(0, last_note_middle_finger, volume)

def middle_finger_stop():
	fs.noteoff(0, last_note_middle_finger)

last_note_ring_finger = ring_finger_note
def ring_finger_start():
	global last_note_ring_finger
	last_note_ring_finger = ring_finger_note+note_additor
	fs.noteon(0, last_note_ring_finger, volume)

def ring_finger_stop():
	fs.noteoff(0, last_note_ring_finger)

last_note_pinky_finger = pinky_finger_note
def pinky_finger_start():
	global last_note_pinky_finger
	last_note_pinky_finger = pinky_finger_note+note_additor
	fs.noteon(0, last_note_pinky_finger, volume)

def pinky_finger_stop():
	fs.noteoff(0, last_note_pinky_finger)

fonts = []
def load_soundfonts():
	global fonts

	BANK = os.path.join(os.path.dirname(__file__), "soundfonts")
	all_files = []
	FILETYPES = ['*.SF2', '*.sf2']
	for filetype in FILETYPES:
		all_files += glob.glob(os.path.join(BANK, filetype))
	print ("{} soundfonts have been found".format(len(all_files)))

	fonts = [fs.sfload(file) for file in all_files]

volume = 0
def set_volume():
	global volume
	new_volume = int(pot0.raw_value / 10)
	if new_volume != volume:
		volume = new_volume
		print("Volume set to {}".format(volume))

# Trigger loading of the sound fonts
load_soundfonts()

instrument = 0
def set_instrument():
	global instrument
	number_of_instruments = len(fonts)-1
	number_of_pot_steps = 1024
	current_pot_value = pot1.raw_value

	new_instrument = int(round(number_of_instruments*(current_pot_value / number_of_pot_steps)))
	#print("Number of instruments: {} / Current pot: {} / New instrument: {} / Number of pot steps: {}".format(number_of_instruments, current_pot_value, new_instrument, number_of_pot_steps))

	if new_instrument != instrument:
		print("Instrument being set to {}".format(new_instrument))
		instrument = new_instrument
		fs.program_select(0, fonts[instrument], 0, 0)

note_additor = 0
def set_note_additor():
	global note_additor
	max_additor = 34
	number_of_pot_steps = 1024
	current_pot_value = pot2.raw_value

	new_additor = int(round(max_additor*(current_pot_value / number_of_pot_steps)))

	if new_additor != note_additor:
		print("Additor being set to {}".format(new_additor))
		note_additor = new_additor

# Select the first sound font
set_volume()
set_instrument()
set_note_additor()

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
	set_volume()
	set_instrument()
	set_note_additor()

main_loop_stopped = 1
while True:
	pass
