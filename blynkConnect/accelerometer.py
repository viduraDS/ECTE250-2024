import spidev
import time
import math
import argparse
import os
import sys

class ADXL345SPI:
    DATA_FORMAT = 0x31
    DATA_FORMAT_B = 0x0B
    READ_BIT = 0x80
    MULTI_BIT = 0x40
    BW_RATE = 0x2C
    POWER_CTL = 0x2D
    DATAX0 = 0x32

    codeVersion = "0.3"
    timeDefault = 5  # default duration of data stream, seconds
    freqDefault = 5  # default sampling rate of data stream, Hz
    freqMax = 3200  # maximal allowed cmdline arg sampling rate, Hz
    speedSPI = 2000000  # SPI communication speed, bps
    freqMaxSPI = 100000  # maximal possible sampling rate through SPI, Hz
    coldStartSamples = 2  # number of samples to be read before outputting data to console
    coldStartDelay = 0.1  # delay between cold start reads
    accConversion = 2 * 16.0 / 8192.0  # +/- 16g range, 13-bit resolution
    tStatusReport = 1  # time period of status report if data read to file, seconds

    def __init__(self, time_stream=timeDefault, freq_stream=freqDefault, save_file=None):
        self.time_stream = time_stream
        self.freq_stream = freq_stream
        self.save_file = save_file
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = self.speedSPI

    def read_bytes(self, data, count):
        data[0] |= self.READ_BIT
        if count > 1:
            data[0] |= self.MULTI_BIT
        return self.spi.xfer2(data)

    def write_bytes(self, data, count):
        if count > 1:
            data[0] |= self.MULTI_BIT
        self.spi.writebytes(data)

    def setup_sensor(self):
        # Set BW_RATE
        self.write_bytes([self.BW_RATE, 0x0F], 2)
        # Set DATA_FORMAT
        self.write_bytes([self.DATA_FORMAT, self.DATA_FORMAT_B], 2)
        # Set POWER_CTL
        self.write_bytes([self.POWER_CTL, 0x08], 2)

    def read_sensor_data(self):
        # Perform cold start reads to stabilize
        for _ in range(self.coldStartSamples):
            self.read_bytes([self.DATAX0] + [0] * 6, 7)
            time.sleep(self.coldStartDelay)

        delay = 1.0 / self.freq_stream
        samples = int(self.freq_stream * self.time_stream)

        if not self.save_file:
            self._read_to_console(samples, delay)
        else:
            self._read_to_file(samples, delay)

    def _read_to_console(self, samples, delay):
        t_start = time.time()
        for i in range(samples):
            data = self.read_bytes([self.DATAX0] + [0] * 6, 7)
            x = (data[2] << 8) | data[1]
            y = (data[4] << 8) | data[3]
            z = (data[6] << 8) | data[5]
            t = time.time() - t_start
            print(f"time = {t:.3f}, x = {x * self.accConversion:.3f}, y = {y * self.accConversion:.3f}, z = {z * self.accConversion:.3f}")
            time.sleep(delay)

    def _read_to_file(self, samples, delay):
        at = []
        ax = []
        ay = []
        az = []
        t_start = time.time()
        
        with open(self.save_file, 'w') as f:
            f.write("time, x, y, z\n")
            for i in range(samples):
                data = self.read_bytes([self.DATAX0] + [0] * 6, 7)
                x = (data[2] << 8) | data[1]
                y = (data[4] << 8) | data[3]
                z = (data[6] << 8) | data[5]
                t = time.time() - t_start
                f.write(f"{t:.5f}, {x * self.accConversion:.5f}, {y * self.accConversion:.5f}, {z * self.accConversion:.5f}\n")
                time.sleep(delay)

    def close(self):
        self.spi.close()
