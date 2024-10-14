import time
import RPi.GPIO as GPIO
import spidev
import math

from blynk_setup import BlynkSetup
from buzzer import Buzzer


BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Actuators
    buzzer = Buzzer(pin=5)  # GPIO5

    # Create Handlers
    def v0_write_handler(value):
        if int(value[0]) == 1:
            buzzer.buzz_on()
        else:
            buzzer.buzz_off()

    # Register handlers with Blynk
    blynk_setup.register_handler("Connected", lambda: print('Connected to Blynk'))
    blynk_setup.register_handler("V0", v0_write_handler)

    try:
        while True:
            blynk_setup.run()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
