import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
import Queue
from threading import Thread
import time
from Adafruit_ADS1x15 import ADS1x15

#this is how after how many samples a block is saved
block_length=120

#iterator for writing files
block_id=0

#declare the q from library
queue = Queue.Queue()

#spec of Adafruit ADS
sps = 860	#samples per second
#pga = 4096	#programmable gain amplifier
adc = ADS1x15(ic=0x01)	#create class identifing model used

def read_data(samples):
	
       	#this array is for sample & sample_time
	packet=[0,0]

	for x in range (samples):
       		sample = adc.readADCDifferential23(256, sps)*1000
		#sample = adc.readADCSingleEnded(0, pga, sps)	#0mV
		
		timenow=UTCDateTime()
		packet[0]=sample
		packet[1]=timenow

         	#print sample,timenow

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

	
			avg_samplingrate=totaltime/block_length

			print avg_samplingrate
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