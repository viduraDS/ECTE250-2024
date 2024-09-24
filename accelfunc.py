import numpy as np
import time as T  
import math 
from ADXL345 import ADXL345

# Initialize the accelerometer
imu = ADXL345()

def Status(x_data,y_data,z_data):
    Threshold = 10
    Magnitude = (x_data^2 + y_data^2 + z_data^2)^1/2
    if Magnitude > Threshold:
        print("Uh oh")


# Main function
def main():
    start_time = T.time()  # Capture the start time

    time_data = []

    try:
        for i in range(1000):   
            # Get the current time relative to start
            current_time = T.time() - start_time

            x_data = 0
            y_data = 0
            z_data = 0

            # Read accelerometer values
            x_data = imu.getX()
            y_dat = imu.getY() 
            z_data = imu.getZ()
            time_data.append(current_time)

            # Sleep for a short duration to simulate real-time data collection (adjust as needed)
            T.sleep(0.01)



        # Call the plot function after data collection
        Status(time_data, x_data, y_data, z_data)

    except KeyboardInterrupt:
        print("Data collection interrupted")

if __name__ == "__main__":
    main()



