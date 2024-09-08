'''
serial driver for gps module
'''
from serial import Serial               #TODO import pyserial

with Serial('/dev/ttySY0',9600) as uart
    uart.send('hello world')
    print(uart.readline())


class Gps:
    def __init__(self,pin,baudRate):
        self.pin = pin
        self.gpsBaud = baudRate
        GPIO.setup(self.pin, GPIO.OUT)
    def wake_gps(self):
        
    def sleep_gps(self):
    
    def ping_location_again(self):

    def get_number_of_sats(self):
    
    def time_at_last_sample(self):
    
    def get_altitude(self):
    
    def get_latitude(self):
    
    def get_longitude(self):
    
    def gps_fix_good(self):
    
    def get_h_dilution_precision(self):

    def get_h_above_ellipsoid(self):

