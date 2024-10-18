import RPi.GPIO as GPIO
import time

class Haptic:
    def __init__(self, pin, frequency=100): 
        self.pin = pin
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.pin, GPIO.OUT)  
        self.frequency = frequency  
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.pin, GPIO.OUT)  
        self.pwm = GPIO.PWM(self.pin, self.frequency)  
        self.pwm.start(0)  
        
    def set_strength(self, duty_cycle):
        """
        Set the strength of the motor by changing the duty cycle.
        :param duty_cycle: Duty cycle (0-100) where 100 is maximum strength.
        """
        if 0 <= duty_cycle <= 100:
            self.pwm.ChangeDutyCycle(duty_cycle)
            print(f"Setting motor strength to {duty_cycle}%")
        else:
            print("Error: Duty cycle must be between 0 and 100")

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)  # Turn the motor on
        print("Haptic motor ON")

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)  # Turn the motor off
        print("Haptic motor OFF")

    def cleanup(self):
        GPIO.cleanup(self.pin)  # Clean up the pin when done

    def pulse(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("Haptic pulse activated")
        time.sleep(1)
        GPIO.output(self.pin,GPIO.LOW)      

class Buzzer: 
    def __init__(self, pin, frequency=100): # Defaulting the frequency to be 100Hz
        self.pin = pin
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering
        GPIO.setup(self.pin, GPIO.OUT)  # Set the pin as an output
        self.frequency = frequency  # Frequency of PWM signal in Hz
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering
        GPIO.setup(self.pin, GPIO.OUT)  # Set the pin as an output
        self.pwm = GPIO.PWM(self.pin, self.frequency)  # Initialize PWM on the pin
        self.pwm.start(0)  # Start PWM with 0% duty cycle (off)

    def set_strength(self, duty_cycle):
        if 0 <= duty_cycle <= 100:
            self.pwm.ChangeDutyCycle(duty_cycle)
            print(f"Setting buzzer strength to {duty_cycle}%")
        else:
            print("Error: Duty cycle must be between 0 and 100")

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)  # Turn the motor on
        print("Buzzer ON")

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)  # Turn the motor off
        print("Buzzer OFF")

    def cleanup(self):
        GPIO.cleanup(self.pin)  # Clean up the pin when done

    def pulse(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("Buzzer pulse activated")
        time.sleep(1)
        GPIO.output(self.pin,GPIO.LOW)

    def set_freq(self, frequency):
        self.frequency = frequency
        print("Set frequency to {self.frequency}Hz")
 


