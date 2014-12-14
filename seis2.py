import numpy
from obspy.core import Trace,Stream,UTCDateTime

from Adafruit_ADS1x15 import ADS1x15
sps = 16        #samples per second
adc = ADS1x15(ic=0x01)  #create class identifing model used

def read():
	return adc.readADCDifferential23(256, sps)*1000

datapoints = 100

data=numpy.zeros([datapoints],dtype=numpy.int32)

x=0
starttime=UTCDateTime()
print(starttime)
while (port.isOpen()) and (x<datapoints):
	sample = read()
	data[x]=sample
	x=x+1
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

st =Stream([Trace(data=data, header=stats)])

st.write('test.mseed',format='MSEED',encoding='INT32',reclen=512)
