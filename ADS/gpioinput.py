from Adafruit_ADS1x15 import ADS1x15
import time
import numpy as np

pga = 4096
ADS1115 = 0x01
adc = ADS1x15(ic=ADS1115)

print "sps value should be one of: 8, 16, 32, 64, 128, 250, 475, 860, otherwise the value will default to 250"
sps = input("Input sps (Hz):         ")

#print adc.readADCSingleEnded(0, pga, sps), "0mV		", ("%.2f" % (t2-startTime)) , "s"
#print adc.readADCSingleEnded(1, pga, sps), "1mV"
print adc.readADCSingleEnded(2, pga, sps), "2mV"
print adc.readADCSingleEnded(3, pga, sps), "3mV"
print adc.readADCDifferential23(256, sps)*1000
