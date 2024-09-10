import spidev
import time
import math

spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 1000000  # 1 MHz
spi.mode = 0b11  # Mode 3 for ASM330LHB

# ASM330LHB register addresses
WHO_AM_I = 0x0F
CTRL1_XL = 0x10  # Control register for accelerometer
CTRL2_G = 0x11  # Control register for gyroscope

ACCEL_X_LSB = 0x28  # Register for accelerometer X-axis LSB
ACCEL_X_MSB = 0x29  # Register for accelerometer X-axis MSB
ACCEL_Y_LSB = 0x2A  # Register for accelerometer Y-axis LSB
ACCEL_Y_MSB = 0x2B  # Register for accelerometer Y-axis MSB
ACCEL_Z_LSB = 0x2C  # Register for accelerometer Z-axis LSB
ACCEL_Z_MSB = 0x2D  # Register for accelerometer Z-axis MSB

# Function to read register
def read_register(register):
    # Sending the register address with read flag (bit 7 = 1 for read)
    return spi.xfer2([register | 0x80, 0x00])[1]

# Function to initialize the ASM330LHB
def init_device():
    who_am_i = read_register(WHO_AM_I)
    if who_am_i != 0x6B:  # Expected device ID for ASM330LHB
        print(f"Device not found. WHO_AM_I register: {hex(who_am_i)}")
        return False
    else:
        print("Device connected!")
    
    # Accelerometer configuration (enable accelerometer, set output data rate, etc.)
    spi.xfer2([CTRL1_XL, 0x60])  # 104 Hz, 2g, 50 Hz filter
    # Gyroscope configuration (if needed)
    spi.xfer2([CTRL2_G, 0x60])  # 104 Hz, 2000 dps

    return True

def read_accel_data():
    x_lsb = read_register(ACCEL_X_LSB)
    x_msb = read_register(ACCEL_X_MSB)
    y_lsb = read_register(ACCEL_Y_LSB)
    y_msb = read_register(ACCEL_Y_MSB)
    z_lsb = read_register(ACCEL_Z_LSB)
    z_msb = read_register(ACCEL_Z_MSB)

    # Combine the MSB and LSB values
    x = (x_msb << 8) | x_lsb
    y = (y_msb << 8) | y_lsb
    z = (z_msb << 8) | z_lsb

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
