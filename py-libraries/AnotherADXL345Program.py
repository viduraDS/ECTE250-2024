# Import dependencies
try:
    import spidev as SPI
except RuntimeError:
    print("Error importing spidev")
try:
    import time as T
except RuntimeError:
    print("Error importing time")

# ADXL345 Registers
POWER_CTL = 0x2D   # Power control register
DATAX0 = 0x32      # X-Axis Data 0
DATAX1 = 0x33      # X-Axis Data 1
DATAY0 = 0x34      # Y-Axis Data 0
DATAY1 = 0x35      # Y-Axis Data 1
DATAZ0 = 0x36      # Z-Axis Data 0
DATAZ1 = 0x37      # Z-Axis Data 1

# SPI initialization
spi = SPI.SpiDev()        # Create a new SPI object
spi.open(3, 0)               # Open bus 0, device 0 (CS0)
spi.max_speed_hz = 5000      # SPI speed (you can increase this if needed)

# Write to the ADXL345 register
def write_register(register, value):
    spi.xfer2([register, value])

# Read from the ADXL345 register
def read_register(register):
    result = spi.xfer2([register | 0x80, 0x00])  # Read operation with MSB set
    return result[1]

# Read two bytes from a register (for acceleration data)
def read_two_bytes(register):
    low_byte = read_register(register)
    high_byte = read_register(register + 1)
    value = (high_byte << 8) | low_byte  # Combine high and low byte
    if value > 32767:
        value -= 65536  # Convert to signed 16-bit integer
    return value

# Initialize the ADXL345
def powerup_adxl345():
    write_register(POWER_CTL, 0x08)  # Set the device to measurement mode
    write_register(0x31,0x8) #Set full res
# Read acceleration data
def read_acceleration():
    x = read_two_bytes(DATAX0)
    y = read_two_bytes(DATAY0)
    z = read_two_bytes(DATAZ0)
    
    # Convert raw values to Gs
    x_g = x * 0.0039
    y_g = y * 0.0039
    z_g = z * 0.0039
    
    return x_g, y_g, z_g

# Main loop to continuously read acceleration data
if __name__ == "__main__":
    powerup_adxl345()
    
    try:
        while True:
            x, y, z = read_acceleration()
            print(f"X: {x:.3f}g, Y: {y:.3f}g, Z: {z:.3f}g")
            T.sleep(0.1)  # Wait 100ms before the next read
    except KeyboardInterrupt:
        spi.close()  # Close the SPI connection when done
