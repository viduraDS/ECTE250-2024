import RPi.GPIO as GPIO
import serial
import time

class Gps:
    def __init__(self,tx,rx):
        self.tx = tx
        self.rx = rx
        GPIO.setup(self.tx, GPIO.IN)
        GPIO.setup(self.rx, GPIO.OUT)
        ser = serial.Serial("gps-serial", baudrate = 9600, timeout = 1)
    def read_gps(self):
        print("hello")
    def tansmit(self)
        print("victor")


