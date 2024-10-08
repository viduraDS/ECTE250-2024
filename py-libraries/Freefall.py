import numpy as np
import time as T
import math
from ADXL345 import ADXL345

# Initialize the accelerometer
imu = ADXL345()

# Initialize velocity as a global variable
velocity = np.array([0.0, 0.0, 0.0])  # Assume starting from rest

# Parameters for detecting sustained high acceleration
acceleration_threshold = 20.0  # Threshold for high acceleration (adjust as needed)
high_accel_duration_limit = 2.0  # Maximum duration to tolerate high acceleration in seconds
warning_duration_limit = 0.5  # Short duration for a warning before high acceleration

def Status(x, y, z, dt):   
    global velocity

    # Calculate the magnitude of the acceleration
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    
    # Update velocity using numerical integration (v = v + a * dt)
    acceleration = np.array([x, y, z])
    velocity += acceleration * dt

    # Calculate the magnitude of the velocity
    velocity_magnitude = math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)

    # Print the current acceleration magnitude and velocity magnitude
    print(f"Acceleration magnitude: {magnitude}, Velocity magnitude: {velocity_magnitude}")
    
    return magnitude

# Main function
def main():
    global velocity
    high_accel_start_time = None
    last_time = T.time()  # Keep track of the last time step

    try:
        for i in range(1000):   
            # Get the current time
            current_time = T.time()
            dt = current_time - last_time  # Calculate the time step (delta time)
            last_time = current_time

            # Read accelerometer values
            x, y, z = imu.getXYZ()

            # Get acceleration magnitude
            accel_magnitude = Status(x, y, z, dt)  

            # Check if the acceleration exceeds the threshold
            if accel_magnitude > acceleration_threshold:
                if high_accel_start_time is None:
                    high_accel_start_time = current_time  # Start tracking the high acceleration period
                
                high_accel_duration = current_time - high_accel_start_time
                
                # Check if high acceleration persists for too long
                if high_accel_duration > high_accel_duration_limit:
                    print("Warning: High acceleration sustained for too long!")
                    # You can also trigger actions like stopping the process, sending an alert, etc.
                elif high_accel_duration > warning_duration_limit:
                    print("Warning: High acceleration detected for a short time!")
            else:
                # Reset the timer when acceleration is below the threshold
                high_accel_start_time = None
            
            # Sleep for a short duration to simulate real-time data collection (adjust as needed)
            T.sleep(0.01)

    except KeyboardInterrupt:
        print("Data collection interrupted")

if __name__ == "__main__":
    main()

