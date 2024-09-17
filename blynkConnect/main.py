from accelerometer import ADXL345
import RPi.GPIO as GPIO

def main():
    GPIO.setmode(GPIO.BCM)
    
    parser = argparse.ArgumentParser(description="Read data from ADXL345 accelerometer via SPI")
    parser.add_argument("-s", "--save", type=str, help="Save data to specified FILE")
    parser.add_argument("-t", "--time", type=int, default=ADXL345SPI.timeDefault, help="Set duration of data stream in seconds (default: 5s)")
    parser.add_argument("-f", "--freq", type=int, default=ADXL345SPI.freqDefault, help="Set sampling rate in Hz (1 <= FREQ <= 3200)")

    args = parser.parse_args()

    if args.freq < 1 or args.freq > 3200:
        print("Invalid frequency specified. Must be between 1 and 3200 Hz.")
        sys.exit(1)

    bowie = ADXL345SPI(time_stream=args.time, freq_stream=args.freq, save_file=args.save)
    bowie.setup_sensor()

    try:
        bowie.read_sensor_data()
    finally:
        bowie.close()

if __name__ == "__main__":
    main()
