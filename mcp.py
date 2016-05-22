from gpiozero import MCP3008, LED
from time import sleep

pot = MCP3008(channel=3, device=0)
purple_led = LED(24)

purple_led.on()

while True:
	pot_reading = pot.value
	print(pot_reading)
	sleep(0.1)
