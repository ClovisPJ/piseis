import serial
import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
import hashlib

port_name='/dev/ttyACM2'

port = serial.Serial(port_name, 9600, timeout=1)

datapoints = 10

data=numpy.zeros([datapoints],dtype=numpy.int16)
x=1

starttime=UTCDateTime()
print(starttime)
while(port.isOpen()) and x<datapoints:
        sample = port.readline().strip()
        data[x]=sample
        x=x+1
        timenow=UTCDateTime()
        print sample,timenow

stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
         'channel': 'BHZ', 'npts': datapoints, 'sampling_rate': 20,
         'mseed': {'dataquality': 'D'},'starttime': starttime}

st=Stream([Trace(data=data, header=stats)])


hash1=hashlib.md5()
hash1.update(data)
name = hash1.hexdigest()

st.write(name + '.mseed',format='MSEED')
