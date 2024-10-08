import blynklib
import time
import RPi.GPIO as GPIO
import adafruit_adxl34x
import serial
import requests
from epd4in2b import EPD
from epd4in2b import EPD_WIDTH, EPD_HEIGHT
from PIL import Image, ImageDraw, ImageFont
import board
import busio
import adafruit_adxl34x

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
epd = EPD()
epd.init()
epd.Clear()
font = ImageFont.load_default()

# Global state
fall_detected = False

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
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), message, font=font, fill=0)
    epd.display(image)
    epd.sleep()

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
      
        # Detect if freefall has occured
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
