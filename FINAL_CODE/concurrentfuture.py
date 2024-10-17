import time
import RPi.GPIO as GPIO
import busio
import board
import adafruit_adxl34x
from blynk_setup import BlynkSetup
from haptic_buzzer import Haptic, Buzzer
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Canvas, Button
import subprocess

BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

# Initialize components
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
haptic = Haptic(pin=12)
buzzer = Buzzer(pin=13)
blynk = BlynkSetup(auth_token=BLYNK_AUTH)

# GPIO Buttons
BUTTON1_PIN = 16  # Yes
BUTTON2_PIN = 17  # No
BUTTON3_PIN = 7   # SOS

GPIO.setmode(GPIO.BCM)
GPIO.setup([BUTTON1_PIN, BUTTON2_PIN, BUTTON3_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize Tkinter window
root = Tk()
root.title("Elderly Care System")
root.geometry("500x700")
canvas = Canvas(root, width=480, height=640, bg="white")
canvas.pack()

# Function to handle Blynk notifications
def alert_carer():
    """Sends a fall alert to the carer using Blynk."""
    blynk.virtual_write(8, "FALL DETECTED - URGENT")

# Function to display breathing exercises on the screen
def display_breathing_exercise():
    subprocess.run(["python", "breath.py"])

# Function to display medication reminders
def display_medication():
    subprocess.run(["python", "Medication.py"])

# Function to display health screen
def display_health():
    subprocess.run(["python", "health.py"])

# Function to handle fall detection
def handle_fall_detection():
    """Handles the event where a fall is detected."""
    fall_detected = True
    start_time = time.time()

    while fall_detected:
        haptic.pulse()
        buzzer.pulse()

        if GPIO.input(BUTTON1_PIN) == GPIO.HIGH:
            print("Confirmed fall, alerting carer...")
            alert_carer()
            fall_detected = False
        elif GPIO.input(BUTTON2_PIN) == GPIO.HIGH:
            print("False alarm, no fall.")
            fall_detected = False
        elif time.time() - start_time > 30:
            print("No response, alerting carer...")
            alert_carer()
            fall_detected = False

# Function to read accelerometer data
def read_accelerometer():
    """Reads accelerometer data and detects freefall."""
    x, y, z = accelerometer.acceleration
    print(f"Acceleration: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
    if accelerometer.events['freefall']:
        print("Freefall detected, handling fall detection...")
        return True
    return False

# Main function with ThreadPoolExecutor to manage concurrent tasks
def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        last_time = time.time()
        future_fall = None

        try:
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time

                # Schedule accelerometer reading in a separate thread
                if not future_fall or future_fall.done():
                    future_fall = executor.submit(read_accelerometer)

                # If a fall is detected, handle fall detection
                if future_fall.result():
                    executor.submit(handle_fall_detection)

                # Keep the Blynk connection alive
                blynk.run()

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Program stopped by user.")
        finally:
            GPIO.cleanup()

# Tkinter UI with buttons to launch different sections of the system
def create_ui():
    start_button = Button(root, text="Start Fall Detection", command=main)
    start_button.place(x=150, y=600)

    breathing_button = Button(root, text="Breathing Exercise", command=display_breathing_exercise)
    breathing_button.place(x=50, y=200)

    medication_button = Button(root, text="Medication", command=display_medication)
    medication_button.place(x=50, y=300)

    health_button = Button(root, text="Health", command=display_health)
    health_button.place(x=50, y=400)

    # Start Tkinter event loop
    root.mainloop()

# Run the UI
create_ui()
