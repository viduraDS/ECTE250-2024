from time import sleep
from ADXL345 import ADXL345 

def detect_free_fall(threshold=10, time_interval=0.1):
    """
    Continuously monitors the ADXL345 for a free fall event.
    
    Parameters:
    - threshold: Number of consecutive free-fall detections before reporting.
    - time_interval: Time interval (seconds) between successive readings.
    """
    
    imu = ADXL345()  # Initialize the ADXL345 accelerometer
    
    consecutive_free_falls = 0  # Keep track of consecutive free falls

    try:
        while True:
            free_fall, _, _, _ = imu.getInterrupts()  # Only check for free fall
            
            if free_fall:
                consecutive_free_falls += 1
                print(f"Free fall detected {consecutive_free_falls} times")
            else:
                consecutive_free_falls = 0  # Reset if no free fall detected

            # Trigger an alert or response when threshold is reached
            if consecutive_free_falls >= threshold:
                print("ALERT: Free fall detected!")
                break  # or take appropriate action
            
            sleep(time_interval)  # Wait before the next check

    except KeyboardInterrupt:
        print("Free fall detection stopped.")

if __name__ == "__main__":
    detect_free_fall()
