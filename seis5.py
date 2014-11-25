import serial
import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
import Queue
from threading import Thread
import time

#serial input spec
port_name='/dev/ttyACM0'
port = serial.Serial(port_name, 9600, timeout=1)

#this is how after how many samples a block is saved
block_length=10

#iterator for writing files
sample_block_id=1
jitter_block_id=1
queue = Queue.Queue()

#this is the thread
def save_data():
	global block_id
	while True:
		if queue.qsize()=block_length:

			data=numpy.zeros([block_length],dtype=numpy.int16)
			jitter=numpy.zeros([block_length],dtype=numpy.int16)

			for x in range 1 to block_length:
				packet = queue.get()
				data[x] = packet[1]
				jitter[x] = packet[2]
				totaltime=totaltime+packet[2]
				queue.task_done()

	
			avg_samplingrate=totaltime/block_length
			#start time is not proper at the mo
			stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
					'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
					'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			st =Stream([Trace(data=data, header=stats)])
      			jt =Stream([Trace(data=jitter)])
			
			#write block with id from iterator
			to_save.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED')
			to_save.write('mseed/JTR' + str(block_id) + '.mseed',format='MSEED')
			block_id=block_id+1




def read_data():
	starttime=UTCDateTime()
       
	packet=[]
	firsttime=True
	totaltime=0
	lastsample=starttime

	while port.isOpen():
		#loop continues indefinately
	        sample = port.readline().strip()
		timenow=UTCDateTime()
		packet[0]=sample

                sample_time=timenow-lastsample
		packet[1]=sample_time

		lastsample=timenow
                #print sample,timenow

	queue.put(packet)

for x in range(1):
	worker_sample = Thread(target=save_data)
	worker_sample.start()

for x in range(5):
	read_data(32)
