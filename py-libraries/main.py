##
 #  @filename   :   main.cpp
 #  @brief      :   4.2inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

# import epd4in2b
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw
from ADXL345 import *
import time
# from GPS import *

COLORED = 1
UNCOLORED = 0

imu = ADXL345(interrupt_enable=True)
imu.enable_interrupts()
# gps = GPS() 


def main():
    # Create an instance of the ADXL345 class
    adxl345 = ADXL345()

    # Enable double-tap interrupts
    adxl345.enable_interrupts()

    try:
        # Keep the program running to listen for interrupts
        while True:
            pass  # You can perform other tasks here if needed
    except KeyboardInterrupt:
        # Clean up GPIO and close SPI connection on exit
        adxl345.close()

if __name__ == "__main__":
    main()
