'''
spi driver for display
'''
import spidev
import time



EPD_WIDTH = 400
EPD_HEIGHT = 300

WHITE = 0xff #255
GRAY1 = 0xC0 #199
GRAY2 = 0x80 #129
BLACK = 0x00 #000


class EPAPER
    def __init__(self, bus=1, device = 0, frequency)
        self.spi = spidev.SpiDev()
        self.spi.open(bus,device)
        self.spi.max_speed_hz = frequency
        self.clear_screen()
        

        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
    def clear_screen()
        
