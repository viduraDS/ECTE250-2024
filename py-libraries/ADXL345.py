import board
import busio
import digitalio
import adafruit_adxl34x

# Set up SPI interface
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D8)  # Use the appropriate GPIO pin for CS

# Initialize the accelerometer over SPI
accelerometer = adafruit_adxl34x.ADXL345_SPI(spi, cs)

accelerometer.enable_tap_detection(tap_count=1, threshold=20, duration=50)

# In your main loop, check for tap events
while True:
    x, y, z = accelerometer.acceleration
    print(f"Acceleration: X={x:.3f} m/s², Y={y:.3f} m/s², Z={z:.3f} m/s²")
    if accelerometer.events['tap']:
        print("Tap detected!")
    time.sleep(0.1)


