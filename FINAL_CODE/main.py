import time
import RPi.GPIO as GPIO
import spidev
import math
import board
import busio
import adafruit_adxl34x
from blynk_setup import BlynkSetup
from haptic-buzzer import Haptic, Buzzer


BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

def calculate_velocity(x, y, z, delta_time):
    """Calculate velocity from acceleration."""
    velocity = []
    velocity[0] += x * delta_time  # X-axis velocity
    velocity[1] += y * delta_time  # Y-axis velocity
    velocity[2] += z * delta_time  # Z-axis velocity
    return velocity

def alert_carer():
    lat, lon = getLocation()
    addr = getAddr(lat, lon)
    blynk_setup.virtual_write(8, addr)




def main():
    # Initialise GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialise Blynk
    blynk_setup = BlynkSetup(auth_token=BLYNK_AUTH)

    # Initialise Accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    # Initialise Actuators
    haptic = Haptic(pin=12)  # GPIO12
    buzzer = Haptic(pin=12)  # GPIO12

    BUTTON1_PIN = 16 # Yes
    BUTTON2_PIN = 17 # No
    BUTTON3_PIN = 7 # SOS

    fall_detected = False

    def v9_write_handler(value):
        message = value[0]
        print(message)
        # send to screen



    # Register handlers with Blynk
    blynk_setup.register_handler("Connected", lambda: print('Connected to Blynk'))
    blynk_setup.register_handler("V9", v9_write_handler)
    

    try:
        while True:
            blynk_setup.run()

            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            x, y, z = accelerometer.acceleration
            velocity = calculate_velocity(x, y, z, delta_time)
            print(f"Acceleration: X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
            print(f"Velocity: {velocity}")

            if accelerometer.events['freefall']:
                start_time = time.time()
                fall_detected = True
                print('fall detected')
                blynk_setup.virtual_write(6, 255)  # Set Fall Detected indicator to red

            while fall_detected:
                buzzer.pulse()
                haptic.pulse()
                if GPIO.input(BUTTON1_PIN) == GPIO.HIGH: # Actually Fallen
                    fall_detected = False
                    alert_carer()
                elif GPIO.input(BUTTON1_PIN) == GPIO.HIGH: # False Alert
                    fall_detected = False
                    blynk_setup.virtual_write(6, 0)  # Turn fall detected indicator off
                else: # no response - fall detected (wait 30s)
                    dt = time.time - start_time
                    if dt < 30:
                        alert_carer()
                        fall_detected = False
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
