import time
import RPi.GPIO as GPIO
import spidev
import math

from blynk_setup import BlynkSetup
from buzzer import Buzzer
from accelerometer import ADXL345


BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

def detect_fall(adxl345):
    fall_detected = False

    # Constants for fall detection
    acceleration_threshold = 2.0  # Threshold for detecting impact (in g)
    free_fall_threshold = 0.3  # Threshold for free fall (near zero g)
    free_fall_time = 0.2  # Minimum time (in seconds) to consider a free fall
    impact_time = 0.1  # Time to detect impact after free fall

    free_fall_start = None

    while True:
        x_g, y_g, z_g = adxl345.read_acceleration()
        total_acc = math.sqrt(x_g**2 + y_g**2 + z_g**2)

        if total_acc < free_fall_threshold:
            if free_fall_start is None:
                free_fall_start = time.time()
        else:
            if free_fall_start is not None:
                elapsed_time = time.time() - free_fall_start
                if elapsed_time >= free_fall_time:
                    if total_acc > acceleration_threshold:
                        fall_detected = True
                        print("Fall detected! Impact acceleration: {:.2f} g".format(total_acc))
                        break
                free_fall_start = None

        time.sleep(0.1)  # Adjust as necessary

    return fall_detected

def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Sensors
    accelerometer = ADXL345()

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

    # Main Loop for Blynk Connection
    try:
        while True:
            if detect_fall(accelerometer):
                # Handle the fall event (e.g., send a notification)
                print("Handling the fall event...")
                # Add your notification or alerting logic here
                time.sleep(5)  # Prevent multiple detections for the same fall


    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        accelerometer.close()

if __name__ == "__main__":
    main()
