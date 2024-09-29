from ctypes import c_int16
import spidev
import RPi.GPIO as GPIO

# Constants for SPI communication and GPIO pins
DEFAULT_SPI_BUS = 3
DEFAULT_SPI_DEVICE = 0

SPI_BUS = DEFAULT_SPI_BUS
SPI_DEVICE = DEFAULT_SPI_DEVICE

CS_PIN = 4  # Chip Select pin
CS_PIN_MODE = GPIO.OUT

ADXL345_DEFAULT_SPI_BITRATE = int(2e6)  # 2 MHz

# Interrupt pins
INT_PIN1 = 23

# Register addresses
ADXL345_REGISTERS = {
    'DEVID': 0x00,
    'THRESH_TAP': 0x1D,
    'OFSX': 0x1E,
    'OFSY': 0x1F,
    'OFSZ': 0x20,
    'DUR': 0x21,
    'Latent': 0x22,
    'Window': 0x23,
    'THRESH_ACT': 0x24,
    'THRESH_INACT': 0x25,
    'TIME_INACT': 0x26,
    'ACT_INACT_CTL': 0x27,
    'THRESH_FF': 0x28,
    'TIME_FF': 0x29,
    'TAP_AXES': 0x2A,
    'ACT_TAP_STATUS': 0x2B,
    'BW_RATE': 0x2C,
    'POWER_CTL': 0x2D,
    'INT_ENABLE': 0x2E,
    'INT_MAP': 0x2F,
    'INT_SOURCE': 0x30,
    'DATA_FORMAT': 0x31,
    'DATAX0': 0x32,
    'DATAX1': 0x33,
    'DATAY0': 0x34,
    'DATAY1': 0x35,
    'DATAZ0': 0x36,
    'DATAZ1': 0x37,
    'FIFO_CTL': 0x38,
    'FIFO_STATUS': 0x39,
}

def MAKE_INT16(high_byte, low_byte):
    return ((high_byte << 8) | low_byte)

class ADXL345:
    def __init__(self, bitrate=ADXL345_DEFAULT_SPI_BITRATE):
        self.__bitrate = bitrate
        self.__spi_setup()
        self.__setup_registers()
        self.__configure_accelerometer()

    def __spi_setup(self):
        # SPI setup
        self.__spi = spidev.SpiDev()
        self.__spi.open(SPI_BUS, SPI_DEVICE)
        self.__spi.max_speed_hz = self.__bitrate
        self.__spi.mode = 0b11  # CPOL=1, CPHA=1

    def __setup_registers(self):
        # Initialize the register map
        self.regs = ADXL345_REGISTERS

    def __configure_accelerometer(self):
        # Set data rate to 100 Hz
        self.__write_data(self.regs['BW_RATE'], [0x0A])
        # Set data format to full resolution, range +/- 2g
        self.__write_data(self.regs['DATA_FORMAT'], [0x08])
        # Put the device in measurement mode
        self.__write_data(self.regs['POWER_CTL'], [0x08])

    def __write_data(self, addr, data):
        MB = len(data) > 1
        msg = [addr | (0x40 if MB else 0x00)] + data
        self.__spi.xfer2(msg)

    def __read_data(self, addr, length):
        MB = length > 1
        msg = [addr | 0x80 | (0x40 if MB else 0x00)] + [0x00] * length
        return self.__spi.xfer2(msg)[1:]

    def enable_interrupts(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(INT_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(INT_PIN1, GPIO.RISING, callback=self.interrupt_callback, bouncetime=200)

        # Set tap detection parameters
        self.__write_data(self.regs['THRESH_TAP'], [0x30])  # Tap threshold
        self.__write_data(self.regs['DUR'], [0x10])         # Tap duration
        self.__write_data(self.regs['Latent'], [0x20])      # Tap latency
        self.__write_data(self.regs['Window'], [0x30])      # Tap window
        self.__write_data(self.regs['TAP_AXES'], [0x07])    # Enable tap on XYZ axes

        # Enable the double tap interrupt
        self.__write_data(self.regs['INT_ENABLE'], [0x20])  # Enable double tap interrupt
        print("Interrupts for Double Tap enabled.")

    def interrupt_callback(self, channel):
        print("Interrupt detected on channel:", channel)
        # Read the interrupt source
        int_source = self.__read_data(self.regs['INT_SOURCE'], 1)[0]
        if int_source & 0x20:
            print("Double Tap detected!")

    def close(self):
        self.__spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    adxl345 = ADXL345()
    adxl345.enable_interrupts()

    try:
        while True:
            pass  # Main loop can perform other tasks
    except KeyboardInterrupt:
        adxl345.close()


