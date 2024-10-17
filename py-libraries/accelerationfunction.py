import numpy as np
import time as T  
import math 
import board
import busio
import adafruit_adxl34x



def Status(x, y, z, dt):

    velocity = np.array([0.0, 0.0, 0.0])  # Assume starting from rest

    # Calculate the magnitude of the acceleration
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    
    # Update velocity using numerical integration (v = v + a * dt)
    acceleration = np.array([x, y, z])
    velocity += acceleration * dt

    # Calculate the magnitude of the velocity
    velocity_magnitude = math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)

    # Print the current acceleration magnitude and velocity magnitude
    print(f"Acceleration magnitude: {magnitude}, Velocity magnitude: {velocity_magnitude}")

# Main function
def main():
    # Initialize the accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    start_time = T.time()  # Capture the start time
    last_time = start_time  # Keep track of the last time step

    try:
        for i in range(1000):   
            # Get the current time
            current_time = T.time()
            dt = current_time - last_time  # Calculate the time step (delta time)
            last_time = current_time

            # Read accelerometer values
            x, y, z = accelerometer.acceleration

            # Print the current acceleration and velocity
            Status(x, y, z, dt)

            # Sleep for a short duration to simulate real-time data collection (adjust as needed)
            T.sleep(1)

    except KeyboardInterrupt:
        print("Data collection interrupted")

if __name__ == "__main__":
    main()




