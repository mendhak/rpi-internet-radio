import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

while True:
    spi.writebytes([0,0,0])     # turn all lights off
    time.sleep(1)
    spi.writebytes([1,255,254]) # turn all lights on
    time.sleep(1)
