import RPi.GPIO as GPIO
import time 

class Buzzer:
    def __init__ (self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz_on (self):
        GPIO.output(self.pin, GPIO.HIGH)

    def buzz_off (self):
        GPIO.output(self.pin, GPIO.LOW)

    def pwm_setup (self):
        PWM_FREQUENCY = 500   
        GPIO.setmode(GPIO.BCM)
        buzzer = GPIO.PWM(self.pin, PWM_FREQUENCY)
        buzzer.start(0)
        for i in range(100):
            buzzer.ChangeDutyCycle(i)
            time.sleep(0.02)
        buzzer.stop()
        GPIO.cleanup()