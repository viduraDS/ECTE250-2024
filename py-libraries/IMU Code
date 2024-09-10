import spidev
import time
import math

# SPI setup for ADXL345
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 5000000  # 5 MHz (ADXL345 supports up to 5 MHz for SPI)
spi.mode = 0b11  # ADXL345 uses SPI mode 3

# ADXL345 register addresses
DEVID = 0x00        # Device ID register
POWER_CTL = 0x2D    # Power-saving features control
DATA_FORMAT = 0x31  # Data format control
DATAX0 = 0x32       # X-axis data 0
DATAX1 = 0x33       # X-axis data 1
DATAY0 = 0x34       # Y-axis data 0
DATAY1 = 0x35       # Y-axis data 1
DATAZ0 = 0x36       # Z-axis data 0
DATAZ1 = 0x37       # Z-axis data 1

# Function to write to a register
def write_register(register, value):
    spi.xfer2([register, value])

# Function to read from a register
def read_register(register, num_bytes):
    return spi.xfer2([register | 0x80] + [0x00] * num_bytes)[1:]

# Function to initialize ADXL345
def init_device():
    # Check if the device is connected by reading the DEVID register
    devid = read_register(DEVID, 1)[0]
    if devid != 0xE5:  # Expected device ID for ADXL345
        print(f"Device not found. DEVID register: {hex(devid)}")
        return False
    else:
        print("Device connected!")
    
    # Set the device to measure mode
    write_register(POWER_CTL, 0x08)  # Measure mode
    # Set the data format (full resolution, +/- 2g range)
    write_register(DATA_FORMAT, 0x08)

    return True

# Function to read accelerometer data
def read_accel_data():
    x0, x1 = read_register(DATAX0, 2)
    y0, y1 = read_register(DATAY0, 2)
    z0, z1 = read_register(DATAZ0, 2)

    # Combine the MSB and LSB values for each axis
    x = (x1 << 8) | x0
    y = (y1 << 8) | y0
    z = (z1 << 8) | z0

    # Convert to signed 16-bit value
    if x & 0x8000:
        x = x - 0x10000
    if y & 0x8000:
        y = y - 0x10000
    if z & 0x8000:
        z = z - 0x10000

    return x, y, z

# Function to calculate tilt angles (pitch and roll)
def calculate_tilt_angles(x, y, z):
    pitch = math.atan2(x, math.sqrt(y**2 + z**2)) * 180.0 / math.pi
    roll = math.atan2(y, math.sqrt(x**2 + z**2)) * 180.0 / math.pi
    return pitch, roll

# Detect fall or tilt based on threshold
def detect_fall_or_tilt(accel_threshold=5000, tilt_threshold=30):
    x, y, z = read_accel_data()
    magnitude = (x**2 + y**2 + z**2)**0.5

    pitch, roll = calculate_tilt_angles(x, y, z)

    print(f"X: {x}, Y: {y}, Z: {z}, Magnitude: {magnitude}, Pitch: {pitch}, Roll: {roll}")

    if magnitude > accel_threshold:
        print("Fall or sudden motion detected!")
        return True
    if abs(pitch) > tilt_threshold or abs(roll) > tilt_threshold:
        print(f"Tilt detected! Pitch: {pitch}, Roll: {roll}")
        return True
    return False

# Main loop
if __name__ == "__main__":
    if init_device():
        while True:
            if detect_fall_or_tilt():
                print("Alert: Possible fall or tilt detected!")
            time.sleep(0.1)  # Read data every 100 ms
