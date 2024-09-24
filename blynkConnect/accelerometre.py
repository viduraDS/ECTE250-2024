import spidev
import time

# Setup SPI connection
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 5000

# ADXL345 Registers
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32

# Initialize the ADXL345
def init_adxl345():
    spi.xfer2([POWER_CTL, 0x08])  # Set the device to measure mode
    spi.xfer2([DATA_FORMAT, 0x08])  # Set data format to full resolution, +/-2g

# Function to read the ADXL345 data
def read_accel():
    data = spi.xfer2([DATAX0 | 0x80, 0x00, 0x00, 0x00, 0x00, 0x00])
    x = ((data[1] << 8) | data[2])
    y = ((data[3] << 8) | data[4])
    z = ((data[5] << 8) | data[6])

    # Convert to signed integer
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536

    return x, y, z

# Initialize the sensor
init_adxl345()

# Read data in a loop
try:
    while True:
        x, y, z = read_accel()
        print("X: {}, Y: {}, Z: {}".format(x, y, z))
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
