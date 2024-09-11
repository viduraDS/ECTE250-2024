from accelerometer import ADXL345
import RPi.GPIO as GPIO

def main():
    GPIO.setmode(GPIO.BCM)

    bowie = ADXL345()

if __name__ == "__main__":
    main()
