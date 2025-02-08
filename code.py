"""CircuitPython Pressure Transducer Data Logger"""

import time

import adafruit_sdcard
import board
import busio
import digitalio
import storage
from analogio import AnalogIn

# Try except to record or handle any errors that occur
try:

    # gets the analog value from pin A0, this is range 0 - 65536
    analog_in = AnalogIn(board.A0)

    # function to convert the analog value to voltage.
    # the maximum voltage is 5 volts
    def get_voltage(pin):
        return (pin.value * 5.0) / 65536

    # Init LED
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    def blink(s):
        # Blink LED
        led.value = True
        time.sleep(s)
        led.value = False

    # Connect to the card and mount the filesystem.
    cs = digitalio.DigitalInOut(board.SD_CS)
    sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sdcard = adafruit_sdcard.SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    # Use the filesystem as normal! Our files are under /sd

    # Set start time. monotonic is a clock in seconds that runs all the time
    start_time = time.monotonic()

    # Set to the start time so we always start at 0 in the output
    elapsed_time = start_time

    # Start count variable
    count = 0

    # Open file
    # It's possible having the file open for a long time causes issues?
    # But I think if it works it'll record the data more consistently.
    # May not matter very much ¯\_(ツ)_/¯
    with open("/sd/volt_test.txt", "a") as f:
        # CSV output format
        f.write("voltage,elapsed_time,count")
        while True:
            voltage = get_voltage(analog_in)

            # Count is mostly here for a sanity check
            out = f"{voltage:.3f},{elapsed_time:.3f},{count}"

            # Print to console
            print(out)

            # Write to file
            f.write(out)

            # Make sure it's written to disk
            # Optionally only run for every x observations
            # if count % 1 == 0:
            f.flush()

            # Increment counter
            count = count + 1

            # Blink LED successful write
            blink(0.1)

            # Sleep for rest of 1s interval
            time.sleep(0.9)

            # Update time here to start at 0
            elapsed_time = time.monotonic()

except Exception as e:
    message = str(e)

    with open(f"/sd/err_{time.monotonic()}", "w") as err:
        err.write(message)

    raise e
