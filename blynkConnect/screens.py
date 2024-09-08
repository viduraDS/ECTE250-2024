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
    # Pin declaration
    # example ---  left_screen = EPAPER(20,21,16,5,6,26)
    def __init__(self, DIN_PIN, SCLK_PIN, CS_PIN, CMD_PIN, BUSY_PIN, RST_PIN)
        self.dataIn = DIN_PIN
        self.clock = SCLK_PIN
        self.chipSelect = CS_PIN
        self.command = CMD_PIN
        self.busy = BUSY_PIN
        self.reset = RST_PIN
    




#    def __init__(self, bus=1, device = 0, frequency)
#        self.spi = spidev.SpiDev()
#        self.spi.open(bus,device)
#        self.spi.max_speed_hz = frequency
#        self.clear_screen()
        

#        self.reset_pin = epdconfig.RST_PIN
#        self.dc_pin = epdconfig.DC_PIN
#        self.busy_pin = epdconfig.BUSY_PIN
#        self.cs_pin = epdconfig.CS_PIN
    def clear_screen()
        
