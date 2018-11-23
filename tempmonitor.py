#this is a test of the 16 bit adc

import RPi.GPIO as GPIO
import spidev
from time import sleep
from datetime import datetime, timedelta


spi_0 = spidev.SpiDev()
spi_0.open(0, 0) # the second number indicates which SPI pin CE0 or CE1

def read_adc(chan):
    if chan > 7 or chan < 0:
        return -1

    # see table on pg. 9 https://www.analog.com/media/en/technical-documentation/data-sheets/LTC1863L-LTC1867L.pdf
    # for explanation of channel to bit equivalent
    r_0 = spi_0.xfer([132 + 64 * (chan % 2) + 16 * chan // 2, 0]) # TODO come up with a cleaner bitwise equivalent?
    adcout_0 = ((r_0[0] & 255) << 8) + r_0[1]
    return adcout_0

# convert voltage to degrees C (this is based on a quick and dirty two point measurement using cold and hot water)
# temp sensor is NPN transistor, measuring voltage drop between emitter and drain as described here:
# https://www.sensortips.com/featured/get-temperature-sensor-transistor/
# current source is actually a voltage divider from 12v to about 1.15 v, actual conversion is probably nonlinear
# because this is a very non-ideal current source. TODO: find calibration curve using 4+ points
def to_C(voltage):
    return -470 * voltage + 313

buf = []
bsize = 10
sample_period = timedelta(seconds=10)
read_period = 0.2/bsize * sample_period.total_seconds() # sample is average of buffer filled over 20% of sample period
start_time = datetime.now()
log_file = 'logs/temp_log_{}.csv'.format(start_time.strftime('%Y%m%d_%H-%M-%S'))
settings_file = 'logs/temp_log_{}-settings.txt'.format(start_time.strftime('%Y%m%d_%H-%M-%S'))

# log run parameters
with open(settings_file, 'w') as f:
    f.write('buffer_size:\t{}\n'.format(bsize))
    f.write('sample_period:\t{} hh:mm:ss\n'.format(sample_period))
    f.write('read_period:\t{} seconds\n'.format(read_period))
    f.write('log_file:\t{}\n'.format(log_file))

# monitor temperature
try:
    reading = to_C(round(1.0*read_adc(0)/65535*3.3, 6))
    print('current temp: {}'.format(reading))
    last_entry = datetime.now()

    while True:
        reading = to_C(round(1.0*read_adc(0)/65535*3.3, 6))
        buf = buf[-(bsize-1):] + [reading]

        now = datetime.now()
        if now - last_entry > sample_period:
            with open(log_file, 'a') as f:
                f.write('{}, {}\n'.format(now.isoformat(), sum(buf)/len(buf)))
            last_entry = now
    sleep(read_period)

except KeyboardInterrupt:
    pass

spi_0.close()
