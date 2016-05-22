from gpiozero import Button

button_reset = Button(23)
button_shutdown = Button(5)

while True:
	if button_reset.is_pressed:
		print "Reset"
	elif button_shutdown.is_pressed:
		print "Shutdown"
	else:
		print "Nothing pressed"
