
import matplotlib as plt
import numpy as np
import time as T  
import board
import busio
import adafruit_adxl34x

# Initialize the accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)


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
            x, y, z = accelerometer.acceleration
            # Read accelerometer values
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)
            time_data.append(current_time)

            # Sleep for a short duration to simulate real-time data collection (adjust as needed)
            T.sleep(0.01)

        # Call the plot function after data collection
        Plot(time_data, x_data, y_data, z_data)

    except KeyboardInterrupt:
        print("Data collection interrupted")

if __name__ == "__main__":
    main()



