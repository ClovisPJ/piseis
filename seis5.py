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
block_length=120

#iterator for writing files
block_id=1
queue = Queue.Queue()

#this is the thread
def save_data():
	global block_id
	while True:
		#print queue.qsize()
		if queue.qsize()>=block_length:

			data=numpy.zeros([block_length],dtype=numpy.int16)
			jitter=numpy.zeros([block_length],dtype=numpy.int16)
			firsttime=True
			totaltime=0
			sample_time = 0
			
			for x in range (block_length):
				packet = queue.get()
				data[x] = packet[0]
       		        	if firsttime == False:
					timenow=packet[1]
					sample_time=timenow-lastsample
				else:
					starttime=packet[1]
				jitter[x] = sample_time
				firsttime = False
				lastsample=packet[1]
				totaltime=totaltime+sample_time
				queue.task_done()

	
			avg_samplingrate=totaltime/block_length
			print avg_samplingrate
			#start time is not proper at the mo
			stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
					'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
					'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			st =Stream([Trace(data=data, header=stats)])
      			jt =Stream([Trace(data=jitter)])
			
			#write block with id from iterator
			st.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			jt.write('mseed/JTR' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			block_id=block_id+1




def read_data(samples):
	print 'read data called'
	for x in range (samples):
		starttime=UTCDateTime()
       
		packet=[0,0]

		while port.isOpen():
			#loop continues indefinately
	       		sample = port.readline().strip()
			timenow=UTCDateTime()
			packet[0]=sample

			packet[1]=timenow

			#lastsample=timenow
               		#print sample,timenow

			queue.put(packet)




for x in range(1):
	worker_sample = Thread(target=save_data)
	worker_sample.start()


read_data(240)
