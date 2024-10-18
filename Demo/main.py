import time
import RPi.GPIO as GPIO
import spidev
import math
import board
import busio
import adafruit_adxl34x
from blynk_setup import BlynkSetup
from hapticBuzzer import Haptic, Buzzer

BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pins for buttons
    BUTTON1_PIN = 17  # Yes
    BUTTON2_PIN = 27  # No
    BUTTON3_PIN = 22  # SOS
    GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    accelerometer.enable_freefall_detection()

    # Initialise Actuators
    haptic = Haptic(pin=13)  # GPIO13 for haptic feedback
    buzzer = Buzzer(pin=12)  # GPIO12 for buzzer

    fall_detected = False
    blynk_setup.virtual_write(8, "No Fall has been Detected")


    def v9_write_handler(value):
        message = value[0]
        print(message)
        # send to screen

    def v0_write_handler(value):
        blynk_setup.virtual_write(6, 255)  # Set Fall Detected indicator to red
        blynk_setup.virtual_write(8, "No Fall has been Detected")

    # Register handlers with Blynk
    blynk_setup.register_handler("Connected", lambda: print('Connected to Blynk'))
    blynk_setup.register_handler("V9", v9_write_handler)
    blynk_setup.register_handler("V0", v0_write_handler)

    try:
        while True:
            blynk_setup.run()
            x, y, z = accelerometer.acceleration
            print(f"Acceleration: X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")

            # print("Pin: 17 = ", GPIO.input(BUTTON1_PIN))
            # print("Pin: 27 = ", GPIO.input(BUTTON2_PIN))
            # print("Pin: 22 = ", GPIO.input(BUTTON3_PIN))

            if accelerometer.events['freefall']:
                start_time = time.time()
                fall_detected = True
                print('Fall detected')
                blynk_setup.virtual_write(6, 255)  # Set Fall Detected indicator to red

            if GPIO.input(BUTTON3_PIN) == 0:
                blynk_setup.virtual_write(6, 255)  # Set Fall Detected indicator to red
                blynk_setup.virtual_write(8, "The University of Wollongong, Northfields Ave, Wollongong NSW 2500")

            while fall_detected:
                print("Pin: 17 = ", GPIO.input(BUTTON1_PIN))
                print("Pin: 27 = ", GPIO.input(BUTTON2_PIN))
                print("Pin: 22 = ", GPIO.input(BUTTON3_PIN))
                buzzer.pulse()
                haptic.pulse()
                if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Actually Fallen
                    fall_detected = False
                    blynk_setup.virtual_write(8, "The University of Wollongong, Northfields Ave, Wollongong NSW 2500")
                elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # False Alert
                    fall_detected = False
                    blynk_setup.virtual_write(6, 0)  # Turn fall detected indicator off
                else:  # No response - fall detected (wait 30s)
                    dt = time.time() - start_time
                    print(dt)
                    if dt > 30:
                        blynk_setup.virtual_write(8, "The University of Wollongong, Northfields Ave, Wollongong NSW 2500")
                        fall_detected = False

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

