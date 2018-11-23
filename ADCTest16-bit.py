#this is a test of the 16 bit adc

import RPi.GPIO as GPIO
import spidev
from time import sleep

print "Start"

spi_0 = spidev.SpiDev()
#spi_0.bits_per_word = 8
spi_0.open(0,0) # the second number indicates which SPI pin CE0 or CE1
#to_send = [0x01,0x02,0x03] #speed Hz, Delay, bits per word
#spi_0.xfer(to_send)
print "here"

def readadc_0(chan):
    if chan > 7 or chan < 0:
        return -1

    #r_0 = spi_0.xfer([1,8 + adcnum_0 << 4, 0]) # start bit, Single/Differntial mode, don't care bit OR
    #r_0 = spi_0.xfer([1,128 + (adcnum_0 << 3),0])
    #r_0 = spi_0.xfer([0x84,0x00])#132 and 196
    # r_0 = spi_0.xfer([0b10000100,0]) # binary literal '0b' + 7 bit input data-word + 0 (not sure why the 0),
    r_0 = spi_0.xfer([132 + 64 * (chan % 2) + 16 * chan // 2, 0]) # come up with a cleaner bitwise equivalent
    # print r_0
    adcout_0 = ((r_0[0] & 255) << 8) + r_0[1]
    #adcout_0 = (r_0[0] << 8) + r_0[1]
    #print r_0
    return adcout_0

buffer = []
bsize = 10

try:
    while True:
        # for i in range(7):
	   # print '{} {}'.format(i, readadc_0(i))
	sleep(.1)
        reading = round(1.0*readadc_0(0)/65535*3.3,6)
        buffer = buffer[-(bsize-1):] + [reading]
	print("avg: {}".format(sum(buffer)/bsize))

except KeyboardInterrupt:
    print "interupted"

print "here"

spi_0.close()
