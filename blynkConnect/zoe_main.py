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

def calculate_velocity(x, y, z, delta_time):
    """Calculate velocity from acceleration."""
    velocity = []
    velocity[0] += x * delta_time  # X-axis velocity
    velocity[1] += y * delta_time  # Y-axis velocity
    velocity[2] += z * delta_time  # Z-axis velocity
    return velocity

def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    # Initialise Actuators
    buzzer = Buzzer(pin=5)  # GPIO5

    fall_detected = False

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
            velocity = calculate_velocity(x, y, z, delta_time)
            print(f"Acceleration: X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
            print(f"Velocity: {velocity}")

            if accelerometer.events['freefall']:
                fall_detected = True
                print('fall detected')
                blynk_setup.virtual_write(6, 1)  # Set Fall Detected indicator (V6) to red

            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            x, y, z = accelerometer.acceleration

            # Calculate velocity


            blynk_setup.virtual_write(8, f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
