import blynklib 
import time
import RPi.GPIO as GPIO
import adafruit_adxl34x
import serial
import requests
from soonuse_paper import Epaper_4in2  # Import Soonuse STM32 Paper Library for 4.2 inch e-paper
from PIL import Image, ImageDraw, ImageFont
import board
import busio

BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'
GOOGLE_MAPS_API_KEY = 'AIzaSyBrcCsgn8itcgdn0XhrkgAG-nUOm7kaX1o'

# GPIO pins
BUTTON_1_PIN = 17
BUTTON_2_PIN = 27
BUZZER_PIN = 22

# Setup Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Setup Accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Setup GPS
gps_serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# Setup E-Paper
epaper = Epaper_4in2()  # Initialize the 4.2 inch e-paper display
epaper.init()
epaper.Clear(0xFF)  # Clear the display to white
font = ImageFont.load_default()

# Global state
fall_detected = False
velocity = [0, 0, 0]  # Velocity in X, Y, Z axes
last_time = time.time()

# High acceleration detection
HIGH_ACCEL_THRESHOLD = 15  # Threshold in m/s^2 (adjust this value as needed)
high_accel_event = False
event_start_time = None
event_duration = 0

def get_acceleration():
    """Get acceleration data from ADXL345."""
    accel_x, accel_y, accel_z = accelerometer.acceleration
    return accel_x, accel_y, accel_z

def calculate_velocity(acceleration, delta_time):
    """Calculate velocity from acceleration."""
    global velocity
    velocity[0] += acceleration[0] * delta_time  # X-axis velocity
    velocity[1] += acceleration[1] * delta_time  # Y-axis velocity
    velocity[2] += acceleration[2] * delta_time  # Z-axis velocity
    return velocity

def detect_high_acceleration(acceleration):
    """Detect if high acceleration event occurs and calculate event duration."""
    global high_accel_event, event_start_time, event_duration

    # Check if any axis exceeds the high acceleration threshold
    if abs(acceleration[0]) > HIGH_ACCEL_THRESHOLD or abs(acceleration[1]) > HIGH_ACCEL_THRESHOLD or abs(acceleration[2]) > HIGH_ACCEL_THRESHOLD:
        if not high_accel_event:  # If it's the start of the event
            high_accel_event = True
            event_start_time = time.time()  # Record the start time of the event
            print("High acceleration event started")
        else:
            event_duration = time.time() - event_start_time  # Calculate duration of ongoing event
            print(f"High acceleration duration: {event_duration:.2f} seconds")
    else:
        if high_accel_event:  # If the event has ended
            high_accel_event = False
            event_duration = time.time() - event_start_time  # Final event duration
            print(f"High acceleration event ended, lasted {event_duration:.2f} seconds")
            display_message_on_epaper(f"High Accel Event: {event_duration:.2f} sec")
            blynk.virtual_write(7, f"High Acceleration Event: {event_duration:.2f} sec")  # Send event info to Blynk
            event_duration = 0  # Reset for next event

def get_gps_coordinates():
    gps_serial.write(b'AT+CGPSINFO\r\n')
    time.sleep(2)
    response = gps_serial.readline().decode('utf-8')
    if "," in response:
        parts = response.split(",")
        if len(parts) > 1:
            latitude = parts[1]
            longitude = parts[3]
            return latitude, longitude
    return None, None

def get_address_from_coordinates(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data['results']) > 0:
            return data['results'][0]['formatted_address']
    return "Address not found"

def display_message_on_epaper(message):
    image = Image.new('1', (epaper.width, epaper.height), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), message, font=font, fill=0)
    epaper.display(image)  # Display the image on the e-paper
epaper.sleep()

# Blynk event handler for text input
@blynk.handle_event('write V9')
def blynk_text_input(pin, values):
    message = values[0]
    display_message_on_epaper(message)

# Blynk event handler for send button
@blynk.handle_event('write V0')
def blynk_send_button(pin, values):
    if values[0] == '1':
        message = blynk.get_value(9)  # Get the message from text input
        display_message_on_epaper(message)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)

# Blynk event handler for device connection
@blynk.handle_event('connected')
def blynk_connected():
    blynk.virtual_write(5, 1)  # Set Device On indicator

try:
    while True:
        blynk.run()
        
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        # Get acceleration data
        acceleration = get_acceleration()

        # Calculate velocity
        velocity = calculate_velocity(acceleration, delta_time)

        # Detect high acceleration event
        detect_high_acceleration(acceleration)

        print(f"Acceleration: {acceleration}")
        print(f"Velocity: {velocity}")
      
        # Detect if freefall has occurred
        if accelerometer.events['freefall']:
            fall_detected = True
            blynk.virtual_write(6, 255)  # Set Fall Detected indicator (V6) to red

        while fall_detected:
          GPIO.output(BUZZER_PIN, GPIO.HIGH)
          
          # Button 1 pressed - Get GPS coordinates and send address to Blynk
          if GPIO.input(BUTTON_1_PIN) == GPIO.LOW and fall_detected:
              latitude, longitude = get_gps_coordinates()
              if latitude and longitude:
                  address = get_address_from_coordinates(latitude, longitude)
                  blynk.virtual_write(8, address)  # Send address to Blynk text box
              GPIO.output(BUZZER_PIN, GPIO.LOW)
              fall_detected = False
              blynk.virtual_write(6, 0)  # Turn fall detected indicator off
  
          # Button 2 pressed - Dismiss fall alert
          if GPIO.input(BUTTON_2_PIN) == GPIO.LOW and fall_detected:
              GPIO.output(BUZZER_PIN, GPIO.LOW)
              fall_detected = False
              blynk.virtual_write(6, 0)  # Turn fall detected indicator off
          GPIO.output(BUZZER_PIN, GPIO.LOW)
          time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
