try:
    while True:


# import dependencies
    try:
        import Rpi.GPIO as GPIO 
    except RuntimeError:
        print("Error importing RPiGPIO")
    try:
        import spidev as SPI
    except RuntimeError:
        print("Error importing spidev")
    try:
        import time as T
    except RuntimeError:
        print("Error importing time")
    try:
        import sys
    except RuntimeError:
        print("Error importing sys"
    try:
        import traceback
    except RuntimeError:
        print("Error importing traceback")
    try:
        import logging
    except RuntimeError:
        print("Error importing logging")
    try:
        import math as M
    except RuntimeError:
        print("Error importing math")



# configure pins
## GPIO
    #refer to pinout.xyz     #using pin numbering, not GPIO numbering
    GPIO_Pins = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,27,28,29,31,32,33,35,36]
    GPIO.setmode(GPIO.BOARD) #Pins 1-40. Use {mode = GPIO.getmode()} to retrieve layout mode in another function
    GPIO.setwarnings(True)
              
        #pin_01,pin_17:3.3v; pin_02,pin_04:5v; pin_06,pin_09,pin_14,pin_20,pin_25 pin_30,pin_34,pin_39:GND;
    IN = [3,5,7]#input pins go here
    GPIO.setup(IN,GPIO.IN,initial=GPIO.HIGH,pull_up_down=GPIO.PUD_UP)

    OUT = [8,10,11]#output pins go here
    GPIO.setup(OUT,GPIO.OUT,initial=GPIO.LOW)

    def GPIO_callback(GPIO_Pins)
        print("detected state change on GPIO pin")
    GPIO.add_event_detect(GPIO_Pins,GPIO.RISING,callback=GPIO_callback


     
              #`GPIO2 code goes here
            
    GPIO.add_event_detect(3, GPIO.RISING, callback=pin_03, bouncetime=200)
   
    GPIO.setup(5, GPIO.IN, initial=GPIO.HIGH, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(5, GPIO.RISING, callback=pin_05, bouncetime=200)
    
    GPIO.setup(7, GPIO.IN, initial=GPIO.HIGH, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(7, GPIO.RISING, callback=pin_07, bouncetime=200)
    
    GPIO.setup(8, GPIO.IN, initial=GPIO.HIGH, pull_up_down=GPIO.PUD_UP) 
    GPIO.add_event_detect(8, GPIO.RISING, callback=pin_08, bouncetime=200)
   

## SPI
    
## UART
    UART_Pins = (1,1)
# debug logger
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)  s - %(messag)s')

# function definitions


def main():
    print("works")

if __name__ = __main__
    main()






except KeyboardInterrupt:
    raise Exception('quitting MAIN_PROGRAM')
    GPIO.cleanup()
    sys.exit()





