import RPi.GPIO as GPIO

class Buzzer:
    def __init__ (self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz_on (self):
        GPIO.output(self.pin, GPIO.HIGH)

    def buzz_off (self):
        GPIO.output(self.pin, GPIO.LOW)