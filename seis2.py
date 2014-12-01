import serial
import numpy
from obspy.core import read,Trace,Stream,UTCDateTime

port_name= '/dev/ttyACM0'

port = serial.Serial(port_name, 9600, timeout=1)

datapoints = 100

data=numpy.zeros([datapoints],dtype=numpy.int32)

x=0
starttime=UTCDateTime()
print(starttime)
while (port.isOpen()) and (x<datapoints):
	sample = port.readline().strip()
	data[x]=sample
	x=x+1
	timenow=UTCDateTime()
	print sample,timenow

stats= {'netwrok': 'UK',
		'station': 'Test',
		'location': '00',
		'channel': 'BHZ',
		'npts': datapoints,
		'sampling_rate': '20',
		'mseed' : {'dataquality' : 'D'},
		'starttime': starttime}

st =Stream([Trace(data=data, header=stats)])

st.write('test.mseed',format='MSEED',encoding='INT32',reclen=512)
#st.plot()
