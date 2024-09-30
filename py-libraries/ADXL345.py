import spidev
import time
import RPi.GPIO as GPIO

# Set up GPIO for interrupt pin (GPIO 23)
INTERRUPT_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTERRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize SPI for SPI3 (bus 3, device 0)
spi = spidev.SpiDev()
spi.open(3, 0)  # SPI3 (Chip Select on GPIO 0)
spi.max_speed_hz = 5000000  # 5 MHz speed
spi.mode = 0b11  # SPI mode 3 (CPOL=1, CPHA=1)

# Helper functions to read/write registers
def write_register(register, value):
    # Write to a register (bit 7 = 0)
    spi.xfer2([register & 0x7F, value])

def read_register(register):
    # Read from a register (bit 7 = 1)
    response = spi.xfer2([register | 0x80, 0x00])
    return response[1]

def read_multiple_registers(start_register, length):
    # Read multiple bytes starting from a register (bit 7 = 1, bit 6 = 1)
    response = spi.xfer2([start_register | 0xC0] + [0x00] * length)
    return response[1:]

# ADXL345 initialization for single-tap detection
def initialize_adxl345():
    # Power on and set ADXL345 to measure mode (POWER_CTL register, 0x2D)
    write_register(0x2D, 0x08)
    
    # Set data format to full resolution, +/-16g (DATA_FORMAT register, 0x31)
    write_register(0x31, 0x0B)
    
    # Enable single-tap interrupt (INT_ENABLE register, 0x2E)
    write_register(0x2E, 0x40)
    
    # Set tap threshold (THRESH_TAP register, 0x1D)
    write_register(0x1D, 0x30)  # Adjust based on desired sensitivity
    
    # Set tap duration (DUR register, 0x21)
    write_register(0x21, 0x10)  # Adjust duration for tap detection
    
    # Enable tap detection on X, Y, and Z axes (TAP_AXES register, 0x2A)
    write_register(0x2A, 0x07)

# Interrupt handler function
def handle_interrupt(channel):
    # Read the INT_SOURCE register (0x30) to check the source of the interrupt
    int_source = read_register(0x30)
    if int_source & 0x40:  # Check if bit 6 is set for tap event
        print("Single tap detected!")

# Initialize ADXL345
initialize_adxl345()

# Add event detection for the interrupt pin (GPIO 23)
GPIO.add_event_detect(INTERRUPT_PIN, GPIO.FALLING, callback=handle_interrupt)

# Main loop to keep the program running
try:
    while True:
        time.sleep(0.1)  # Small delay to keep the program running
except KeyboardInterrupt:
    # Cleanup GPIO and SPI on exit
    GPIO.cleanup()
    spi.close()



