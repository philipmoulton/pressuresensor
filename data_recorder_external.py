#! /usr/bin/env python
# On External Computer

import time

# Requires python package `pyserial` installed
import serial

if __name__ == "__main__":
    # Adjust the serial port name as needed
    # (e.g., 'COM3' on Windows, '/dev/ttyACM0' on Linux)
    # baud rate: 115200
    # https://www.digikey.com/en/htmldatasheets/production/8201480/0/0/1/4884#:~:text=speed%20required%20by%20the%20board%20is%20115200%20bits%20per%20second
    # https://pyserial.readthedocs.io/en/latest/pyserial_api.html
    ser = serial.Serial("/dev/ttyACM0", 115200)

    # Wait for the connection to establish
    time.sleep(2)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            print(line)
