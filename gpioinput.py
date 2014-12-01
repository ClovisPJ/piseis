from Adafruit_ADS1x15 import ADS1x15

sps=860
pga = 4096
adc = ADS1x15(ic=0x01)

print adc.readADCSingleEnded(0, pga, sps), "0mV"
print adc.readADCSingleEnded(1, pga, sps), "1mV"
print adc.readADCSingleEnded(2, pga, sps), "2mV"
print adc.readADCSingleEnded(3, pga, sps), "3mV"
print adc.readADCDifferential23(256, sps)*1000
