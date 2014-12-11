import serial
import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
import Queue
from threading import Thread
import time

#serial input spec
port_name='/dev/ttyACM0'
port = serial.Serial(port_name, 9600, timeout=1)

#number of samples in each mseed file
block_length=128

#iterator for writing files
block_id=1
x=0

#this is needed for saving in mseed so must be passed globably 
global starttime

global block_id

#define the queue from using the library
q = Queue.Queue()


def read_data(block_length):
	starttime=UTCDateTime()
	while (port.isOpen()) and (x<block_length):
		
		#loop continues for block length
	        sample = port.readline().strip()
		
		#'timenow' not essential at the moment and isn't stored
	       	timenow=UTCDateTime()
	       	print sample,timenow
		x=x+1
		q.put(sample)



#this is the worker thread
def save_data():
	while True:
		if (q.qsize()>=block_length):
			data=numpy.zeros([block_length],dtype=numpy.int16)

			for x in range (block_length):	
				sample = q.get()
				data[x]=sample
				q.task_done()
			
			stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
	        		 'channel': 'BHZ', 'npts': block_length, 'sampling_rate': 20,
			         'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			st =Stream([Trace(data=data, header=stats)])
			to_save.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED')
			block_id=block_id+1
		else:
			print 'nothing to save...'



for x in range(1):
	worker = Thread(target=save_data)
	worker.start()

for x in range(50):
	read_data(block_length)
