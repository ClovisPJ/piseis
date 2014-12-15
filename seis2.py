import numpy
from obspy.core import Trace,Stream,UTCDateTime

from Adafruit_ADS1x15 import ADS1x15
sps = 16        #samples per second
adc = ADS1x15(ic=0x01)  #create class identifing model used

data=numpy.zeros([datapoints],dtype=numpy.int16)

datapoints = 100

starttime=UTCDateTime()

for x in range (datapoints):
	sample = adc.readADCDifferential23(256, sps)*1000
	data[x]=sample
	timenow=UTCDateTime()
	print sample,timenow

stats= {'network': 'UK',
		'station': 'Test',
		'location': '00',
		'channel': 'BHZ',
		'npts': datapoints,
		'sampling_rate': '20',
		'mseed' : {'dataquality' : 'D'},
		'starttime': starttime}

stream =Stream([Trace(data=data, header=stats)])

stream.write('test.mseed',format='MSEED',encoding='INT16',reclen=512)
