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
sample_block_id=1
jitter_block_id=1
samplequeue = Queue.Queue()
jitterqueue = Queue.Queue()

#this is the thread
def save_data():
	#it wait as there won't be anything to save in the first 5 seconds
	time.sleep(5)
	global sample_block_id
	while True:
		#'if' not essential but wil allow waiting to save processing
		if not samplequeue.empty():
			to_save = samplequeue.get()
			#write block with id from iterator
			to_save.write('mseed/PHYS' + str(sample_block_id) + '.mseed',format='MSEED')
			sample_block_id=sample_block_id+1
			samplequeue.task_done()
		else:
			print 'nothing to save...'
			#to save processing bit
			time.sleep(5)



def save_data():
	#it wait as there won't be anything to save in the first 5 seconds
	time.sleep(5)
	global jitter_block_id
	while True:
		#'if' not essential but wil allow waiting to save processing
		if not jitterqueue.empty():
			to_save = jitterqueue.get()
			#write block with id from iterator
			to_save.write('mseed/PHYS' + str(jitter_block_id) + '.mseed',format='MSEED')
			jitter_block_id=jitter_block_id+1
			jitterqueue.task_done()
		else:
			print 'nothing to save...'
			#to save processing bit
			time.sleep(5)



def read_data(block_length):
	starttime=UTCDateTime()
	x=1
	data=numpy.zeros([block_length],dtype=numpy.int16)
	jitter=numpy.zeros([block_length],dtype=numpy.int16)
        firsttime=True
	totaltime=0

	while (port.isOpen()) and x<block_length:
		#loop continues for block size
	        sample = port.readline().strip()
		data[x]=sample
		timenow=UTCDateTime()
		
                if firsttime==True:
		    starttime=timenow
		    firsttime=False
		else:
                    sample_time=timenow-starttime
                    jitter[x]=sample_time
		    totaltime=totaltime+sample_time
                
                x=x+1
                print sample,timenow

	avg_samplingrate=totaltime/block_length
	print avg_samplingrate
	stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
	         'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
	         'mseed': {'dataquality': 'D'},'starttime': starttime}
	#create strem of data and queue it
	st =Stream([Trace(data=data, header=stats)])
        jt =Stream([Trace(data=jitter)])
	samplequeue.put(st)
	jitterqueue.put(jt)

for x in range(1):
	worker = Thread(target=save_data)
	#worker.Daemon = True
	worker.start()

for x in range(5):
	read_data(32)
