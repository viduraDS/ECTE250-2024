import numpy as np
import matplotlib as plt

import matplotlib.pyplot as plt
import numpy as np

# In main 
from ADXL345 import *
import time

imu = ADXL345()

# Plot function

def Plot(x,y,z):
     plt.figure(figsize=(10, 6))
     
     # Plot X-axis acceleration
     plt.plot(time, x, label='X-axis', color='r', linestyle='-')

     # Plot Y-axis acceleration
     plt.plot(time, y, label='Y-axis', color='g', linestyle='-')

      # Plot Z-axis acceleration
     plt.plot(time, z, label='Z-axis', color='b', linestyle='-')

      # Add labels and title
     plt.xlabel('Time (s)')
     plt.ylabel('Acceleration (g)')
     plt.title('Acceleration Data Over Time')

     # Add a legend
     plt.legend()

     # Show the plot
     plt.grid(True)
     plt.show()

try:
    def main():

        while True:
            print("X:",imu.getX())
            print("Y:",imu.getY())
            print("Z:",imu.getZ())
            Plot(imu.getX,imu.getY,imu.getZ)
            time.sleep(0.1)
        return 0
   

except KeyboardInterrupt:
    #imu._ADXL345__power_down()               
    print("penis") 
if __name__ == "__main__":
    main()





