# Raspberry Pi Music Box
# Code by Michael Horne
# Some code based on code written by Pimoroni - https://github.com/pimoroni/Piano-HAT

from gpiozero import Button, MCP3008, LED
import pygame
import signal
import glob
import os
import re
import time

# Set-up sounds for import
BANK = os.path.join(os.path.dirname(__file__), "sounds")
FILETYPES = ['*.wav', '*.ogg']
samples = []
files = []
octave = 0
octaves = 0

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

# Start-up music
play_startup = 1
if play_startup:
	pygame.mixer.music.load("/home/pi/musicbox/startup.mp3")
	pygame.mixer.music.play()
	time.sleep(3)

pygame.mixer.set_num_channels(32)

# Search for patch (wav/ogg) files
patches = glob.glob(os.path.join(BANK, '*'))
patch_index = 0

# Error if nothing found
if len(patches) == 0:
    exit("Couldn't find any .wav files in: {}".format(BANK))

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

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]

def load_samples(patch):
    global samples, files, octaves, octave
    files = []
    print('Loading Samples from: {}'.format(patch))
    for filetype in FILETYPES:
        files.extend(glob.glob(os.path.join(patch, filetype)))
    files.sort(key=natural_sort_key)
    octaves = len(files) / 12
    samples = [pygame.mixer.Sound(sample) for sample in files]
    octave = int(octaves / 2)

def play_note(note):
    global samples
    samples[note].play(loops=0)

def handle_instrument(channel, pressed):
    global patch_index
    patch_index += 1
    patch_index %= len(patches)
    print('Selecting Patch: {}'.format(patches[patch_index]))
    load_samples(patches[patch_index])

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

#pianohat.on_note(handle_note)
# Load the piano samples
load_samples(patches[1])

# Give some diagnostic information
print("RASPBERRY PI MUSIC BOX")
print("There are {} octaves".format(octaves))
print("There are {} samples".format(len(samples)))

# Set-up main loop watchers
main_loop_stopped = 0
stop_main_loop = 0

print("Initialising rear buttons")
button_reset.when_pressed = reset
button_shutdown.when_pressed = shutdown

note_multiplier = 4

def trigger_note(finger, note_value):
	global note_multiplier

	while finger.is_pressed:
		play_note(note_value * note_multiplier)

def play_index_finger():
	global index_finger
	trigger_note(index_finger, 2)

def play_middle_finger():
	global middle_finger
	trigger_note(middle_finger, 4)

def play_ring_finger():
	global ring_finger
	trigger_note(ring_finger, 6)

def play_pinky_finger():
	global pinky_finger
	trigger_note(pinky_finger, 8)

index_finger.when_pressed = play_index_finger
middle_finger.when_pressed = play_middle_finger
ring_finger.when_pressed = play_ring_finger
pinky_finger.when_pressed = play_pinky_finger

print("Starting main loop")
# Main loop
while not stop_main_loop:
	pass
	#print("Pot 0: {} / Pot 1: {} / Pot 2: {}".format(pot0.value, pot1.value, pot2.value))	
	#time.sleep(0.5)

	#for chan in [0,1,2,3,4,5,6,7,8]:
	#	play_note(chan)
	#	time.sleep(0.4)

main_loop_stopped = 1
while True:
	pass
