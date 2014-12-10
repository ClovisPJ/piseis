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
block_id=0

#declare the q from library
queue = Queue.Queue()

def read_data(samples):
	for x in range (samples):
       		#this array is for sample & sample_time
		packet=[0,0]

	       	sample = port.readline().strip()
		timenow=UTCDateTime()
		packet[0]=sample
		packet[1]=timenow

             	print sample,timenow

		queue.put(packet)



#this is the worker thread
def save_data():
	global block_id
	while True:
		#print queue.qsize()
		if (queue.qsize()>=block_length):

			#two arrays for reading samples & jitter into
			data=numpy.zeros([block_length],dtype=numpy.int16)
			jitter=numpy.zeros([block_length],dtype=numpy.int16)

			firsttime=True
			totaltime=0
			sample_time = 0
			
			for x in range (block_length):
				packet = queue.get()
				data[x] = packet[0]
				
				#firsttime check is essential to get 'starttime' for mseed header
       		        	if firsttime == True:
					starttime=packet[1]
					firsttime = False
				else:
					sample_time=packet[1]
					sample_difference=sample_time- previous_sample

				jitter[x] = sample_difference
				
				#previos_sample is used to get the difference in the next loop
				previous_sample=packet[1]

				totaltime=totaltime+sample_difference
				queue.task_done()

	
			avg_samplingrate=1/(totaltime/block_length)

			#print avg_samplingrate
			stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
					'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
					'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			st =Stream([Trace(data=data, header=stats)])
      			jt =Stream([Trace(data=jitter)])
			
			#write block with id from iterator
			st.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			jt.write('mseed/JTR' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			block_id=block_id+1




for x in range(1):
	worker_sample = Thread(target=save_data)
	worker_sample.start()


read_data(block_length)
