from ADXL345 import *
import time


imu = ADXL345()
try:
    def main():

        while True:
            print("X:",imu.getX())
            print("Y:",imu.getY())
            print("Z:",imu.getZ())
            time.sleep(0.1)
        return 0


    

except KeyboardInterrupt:
    #imu._ADXL345__power_down()               
    print("penis") 
if __name__ == "__main__":
    main()

