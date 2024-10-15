import time
import RPi.GPIO as GPIO
import spidev
import math
import board
import busio
import adafruit_adxl34x
from blynk_setup import BlynkSetup
from buzzer import Buzzer


BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    accelerometer.enable_freefall_detection()

    # Initialise Actuators
    buzzer = Buzzer(pin=5)  # GPIO5

    # Create Handlers
    def v0_write_handler(value):
        if int(value[0]) == 1:
            buzzer.buzz_on()
        else:
            buzzer.buzz_off()

    def v8_write_handler(value):
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
            if accelerometer.events['freefall']:
                fall_detected = True
                print('fall detected')
                blynk_setup.virtual_write(6, 255)  # Set Fall Detected indicator (V6) to red
            x, y, z = accelerometer.acceleration
            blynk_setup.virtual_write(8, f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
