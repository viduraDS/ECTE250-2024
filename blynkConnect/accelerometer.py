import spidev
import time

class ADXL345:
    # ADXL345 Registers
    THRESH_TAP = 0X1D #Tap threshold
    OFSX = 0X1E #X-axis offset
    OFSY = 0X1F #Y-axis offset
    OFSZ = 0X20 #Z-axis offset
    DUR = 0X21 #Tap duration
    Latent = 0x22 #Tap latency
    Window = 0x23 #Tap window
    THRESH_ACT = 0X24 #Activity threshold
    THRESH_INACT = 0X25 #Inactivity threshold
    TIME_INACT = 0X26 #Inactivity time
    ACT_INACT_CTL =  0X27 #Axis enable control for activity and inactivity detection
    
    THRESH_FF = 0X28 #Free-fall threshold

    TIME_FF = 0X29 #Free-fall time

    TAP_AXES = 0X2A #Axis control for single tap/double tap
    ACT_TAP_STATUS = 0X2B #Source of single tap/double tap
    BW_RATE = 0X2C #Data rate and power mode control
    POWER_CTL = 0X2D #Power-saving features control
    INT_ENABLE = 0X2E #Interrupt enable control
    INT_MAP = 0X2F #Interrupt mapping control
    INT_SOURCE = 0X30 #Source of interrupts
    DATA_FORMAT = 0x31 #Data format control
    DATAX0 = 0x32 #X-Axis Data 0
    DATAX1 = 0X33 #X-Axis Data 1
    DATAY0 = 0X34 #Y-Axis Data 0
    DATAY1 = 0X35 #Y-Axis Data 1
    DATAZ0 = 0X36 #Z-Axis Data 0
    DATAZ1 = 0X37 #Z-Axis Data 1
    FIFO_CTL = 0X38 #FIFO control
    FIFO_STATUS = 0X39 #FIFO status


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
        x = ((data[0] << 8) | data[1])
        y = ((data[2] << 8) | data[3])
        z = ((data[4] << 8) | data[5])

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
