from ADXL345 import *
import time


imu = ADXL345()
try:
    def main():

        while True:
            print("X:",imu.getX())
            print("Y:",imu.getY())
            print("Z:",imu.getZ())
            print("Free Fall :",imu.getInterupts()[0])
            print("Activity: ",imu.getInterupts()[1])
            print("DoubleTap: ",imu.getInterupts()[2])
            print("SingleTap: ",imu.getInterupts()[3])
            time.sleep(1)
        return 0


    

except KeyboardInterrupt:
    #imu._ADXL345__power_down()               
    print("penis") 
if __name__ == "__main__":
    main()

