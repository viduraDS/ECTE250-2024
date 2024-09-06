import spidev
import time

class ADXL345:
    # ADXL345 Registers
    POWER_CTL = 0x2D
    DATA_FORMAT = 0x31
    DATAX0 = 0x32

    def __init__(self, bus=0, device=0, max_speed_hz=5000):
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)  # Open SPI bus and device (CS)
        self.spi.max_speed_hz = max_speed_hz
        self.init_sensor()


    def init_sensor(self):
        # Initialize the ADXL345 sensor
        self.spi.xfer2([self.POWER_CTL, 0x08])  # Set to measure mode
        self.spi.xfer2([self.DATA_FORMAT, 0x08])  # Set to full res, +/-2g

    def read_raw_data(self):
        # Read raw data
        data = self.spi.xfer2([self.DATAX0 | 0x80, 0x00, 0x00, 0x00, 0x00, 0x00])
        x = ((data[1] << 8) | data[2])
        y = ((data[3] << 8) | data[4])
        z = ((data[5] << 8) | data[6])

        # Convert to signed integer
        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536

        return x, y, z

    def read_acceleration(self):
        # Read acceleration data from the ADXL345 sensor
        x, y, z = self.read_raw_data()

        scale_factor = 0.0039  # Assuming +/-2g range and full res
        x_g = x * scale_factor
        y_g = y * scale_factor
        z_g = z * scale_factor

        return x_g, y_g, z_g

    def close(self):
        # Close the SPI connection
        self.spi.close()
