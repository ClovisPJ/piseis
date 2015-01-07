import numpy
from obspy.core import read,Trace,Stream,UTCDateTime
import Queue
from threading import Thread
import os.path

from Adafruit_ADS1x15 import ADS1x15
sps = 16        #samples per second
adc = ADS1x15(ic=0x01)  #create class identifing model used

#this is how after how many samples a block is saved
block_length=224

#directories for data
mseed_directory = 'mseed'
jitter_directory = 'jitter'

#declare the q from library
queue = Queue.Queue()

def read_data():
	while True:
		#this array is for sample & sample_time
		packet=[0,0]

		sample = adc.readADCDifferential23(256, sps)*1000
		timenow=UTCDateTime()
		
		packet[0]=sample
		packet[1]=timenow

		print sample,timenow

		queue.put(packet)



#this is the worker thread
def save_data():
	while True:
		if queue.qsize()>=block_length:

			#two arrays for reading samples & jitter into
			data=numpy.zeros([block_length],dtype=numpy.int16)
			#note jitter uses float32 - decimals
			jitter=numpy.zeros([block_length],dtype=numpy.float32)

			firsttime=True
			totaltime=0
			sample_time = 0
			sample_difference = 0
			
			#this is the loop without storing jitter value and calcs
			packet = queue.get()
			data[0] = packet[0]
			starttime = packet[1]
			
			previous_sample=packet[1]
			queue.task_done()

			for x in range (1,block_length):
				packet = queue.get()
				data[x] = packet[0]
				
				sample_time=packet[1]
				sample_difference=sample_time- previous_sample

				#as sps is a rate, and s.d. is time, its 1 over sps
				jitter[x] = sample_difference - (1/sps)
				
				#previos_sample is used to get the difference in the next loop
				previous_sample=packet[1]

				totaltime=totaltime+sample_difference
				queue.task_done()

	
			#a.s.r. is a rate, and t.t is time so its 1 over
			avg_samplingrate = 1 / (totaltime/block_length)
			stats = {'network': 'UK', 'station': 'RASPI', 'location': '00',
					'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
					'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			sample_stream =Stream([Trace(data=data, header=stats)])
			jitter_stream =Stream([Trace(data=jitter)])

			#write sample data
			File = mseed_directory + '/' + str(sample_stream[0].stats.starttime.date) + '.mseed'
			if os.path.isfile(File):
				total_stream = read(File)

				#as when the data is read it is not in the correct format
				for i in range (total_stream.count()):	
					total_stream[i].data = total_stream[i].data.astype(numpy.int16)

				total_stream += sample_stream
				total_stream.write(File,format='MSEED',encoding='INT16',reclen=512)
			else:
			#if this is the first block
				sample_stream.write(File,format='MSEED',encoding='INT16',reclen=512)


			#write jitter data
			#File = jitter_directory + '/' + str(jitter_stream[0].stats.starttime.date) + '.mseed'
			#if os.path.isfile(File):
			#	total_stream = read(File)

			#	for i in range (total_stream.count()):	
			#		total_stream[i].data = total_stream[i].data.astype(numpy.int16)
					
			#	total_stream += jitter_stream
			#	total_stream.write(File,format='MSEED',encoding='FLOAT32',reclen=512)
			#else:
			#	jitter_stream.write(File,format='MSEED',encoding='FLOAT32',reclen=512)



worker_sample = Thread(target=save_data)
worker_sample.start()

read_data()
