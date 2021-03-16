# coding:utf-8
import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def readAdc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def convertVolts(data):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,4)
    return volts

def convertTemp(volts):
    temp = (100 * volts) - 50.0
    temp = round(temp,4)
    return temp

if __name__ == '__main__':
    try:
        while True:
            data = readAdc(0)
            print("adc  : {:8} ".format(data))
            volts = convertVolts(data)
            temp = convertTemp(volts)
            print("volts: {:8.2f}".format(volts))
            print("temp : {:8.2f}".format(temp))

            time.sleep(5)
    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)