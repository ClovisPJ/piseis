import serial
import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
#import hashlib
import Queue
from threading import Thread
import time

#serial input spec
port_name='/dev/ttyACM0'
port = serial.Serial(port_name, 9600, timeout=1)

#array of zeros to write data into
#block_length=0

#iterator for writing files
block_id=1
q = Queue.Queue()

#this is the thread
def save_data():
	#it wait as there won't be anything to save in the first 5 seconds
	time.sleep(5)
	global block_id
	while True:
		#'if' not essential but wil allow waiting to save processing
		if not q.empty():
			to_save = q.get()
			#write block with id from iterator
			to_save.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED')
			block_id=block_id+1
			q.task_done()
		else:
			print 'nothing to save...'
			#to save processing bit
			time.sleep(5)


def read_data(block_length):
	starttime=UTCDateTime()
	x=1
	data=numpy.zeros([block_length],dtype=numpy.int16)
	firsttime=true
	
	while (port.isOpen()) and x<block_length:
		#loop continues for block size
	        sample = port.readline().strip()
		data[x]=sample
	       	x=x+1
		#'timenow' not essential and isn't stored
		if firsttime=true:
			starttime=timenow
			firsttime=false
		else:
			totaltime=totaltime+(timenow-starttime)


		timenow=UTCDateTime()
	       	print sample,timenow

	avg_samplingrate=totaltime/block_length
	print avg_samplingrate
	stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
	         'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
	         'mseed': {'dataquality': 'D'},'starttime': starttime}
	#create strem of data and queue it
	st =Stream([Trace(data=data, header=stats)])
	q.put(st)

for x in range(1):
	worker = Thread(target=save_data)
	#worker.Daemon = True
	worker.start()

for x in range(50):
	read_data(128)
