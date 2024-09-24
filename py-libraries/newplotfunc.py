
import matplotlib.pyplot as plt
import time as T  
from ADXL345 import ADXL345

# Initialize the accelerometer
imu = ADXL345()

# Plot function
def Plot(time_data, x, y, z):
    plt.figure(figsize=(10, 6))
    
    # Plot X-axis acceleration
    plt.plot(time_data, x, label='X-axis', color='r', linestyle='-')

    # Plot Y-axis acceleration
    plt.plot(time_data, y, label='Y-axis', color='g', linestyle='-')

    # Plot Z-axis acceleration
    plt.plot(time_data, z, label='Z-axis', color='b', linestyle='-')

    # Add labels and title
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('Acceleration Data Over Time')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.savefig('Data.png')

# Main function
def main():
    x_data = []
    y_data = []
    z_data = []
    time_data = []

    start_time = T.time()  # Capture the start time

    try:
        for i in range(1000):   
            # Get the current time relative to start
            current_time = T.time() - start_time

            # Read accelerometer values
            x_data.append(imu.getX())
            y_data.append(imu.getY())
            z_data.append(imu.getZ())
            time_data.append(current_time)

            # Sleep for a short duration to simulate real-time data collection (adjust as needed)
            T.sleep(0.01)

        # Call the plot function after data collection
        Plot(time_data, x_data, y_data, z_data)

    except KeyboardInterrupt:
        print("Data collection interrupted")

if __name__ == "__main__":
    main()



