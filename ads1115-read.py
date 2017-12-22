import time
import datetime
import signal
import sys

from sys import stdout
# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 16

# Start continuous ADC conversions on channel 0 using the previously set gain
# value.  Note you can also pass an optional data_rate parameter, see the simpletest.py
# example and read_adc function for more infromation.
adc.start_adc(0, gain=GAIN, data_rate=860)
# Once continuous ADC conversions are started you can call get_last_result() to
# retrieve the latest result, or stop_adc() to stop conversions.

def to_unix_timestamp(ts):
    """
    Get the unix timestamp (seconds from Unix epoch)
    from a datetime object
    """
    start = datetime.datetime(year=1970, month=1, day=1)
    diff = ts - start
    return diff.total_seconds()

def handler(signum, frame):
    print 'Shutting down ADC'
    adc.stop_adc()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

while True:
    n = datetime.datetime.now()
    timestamp = to_unix_timestamp(n)
    value = (adc.get_last_result() * 0.1875)/1000

    print "{},{}".format(timestamp, value)
    stdout.flush()

    time.sleep(0.1)
