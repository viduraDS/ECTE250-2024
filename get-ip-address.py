import os
import socket
import time
from datetime import datetime

# Function to check if the device is connected to the internet
def wait_for_internet(timeout=60, interval=5):
    for _ in range(int(timeout / interval)):
        try:
            # Try to connect to Google's DNS server to check if there's internet access
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            print("Internet connection established.")
            return True
        except OSError:
            print("Waiting for internet connection...")
            time.sleep(interval)
    print("No internet connection after waiting.")
    return False

# Function to get the IP address of the Raspberry Pi
def get_ip_address():
    try:
        # This will get the IP address of the device by connecting to an external host
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Google DNS server used to find the IP
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Unable to get IP address: {e}"

# Function to check if the USB is mounted at /media/flash/
def is_usb_mounted():
    usb_mount_point = '/media/flash/victor/'
    if os.path.ismount(usb_mount_point):
        return usb_mount_point
    return None

# Function to append the IP address with a timestamp to a file on the USB stick
def write_ip_to_usb(ip_address, mount_point):
    try:
        file_path = os.path.join(mount_point, 'rpi_ip_address.txt')
        with open(file_path, 'a') as f:  # 'a' mode for appending to the file
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{current_time} - The local IP address of the Raspberry Pi is: {ip_address}\n")
        print(f"IP address appended to {file_path}")
    except Exception as e:
        print(f"Failed to write to USB: {e}")

# Main function
if __name__ == "__main__":
    # Wait for an internet connection before proceeding
    if wait_for_internet():
        # Get the IP address
        ip_address = get_ip_address()

        # Check if the USB is mounted at /media/flash/
        mount_point = is_usb_mounted()

        if mount_point:
            # Append the IP address with a timestamp to the USB stick
            write_ip_to_usb(ip_address, mount_point)
        else:
            print("No USB stick found or mounted at /media/flash/.")
    else:
        print("Could not establish internet connection. Exiting script.")