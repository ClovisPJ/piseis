from Adafruit_ADS1x15 import ADS1x15
sps = 16        #samples per second
adc = ADS1x15(ic=0x01)  #create class identifing model used

#  this looprints all the data appearing on this port 

while True:
	sample = adc.readADCDifferential23(256, sps)*1000
	print sample
