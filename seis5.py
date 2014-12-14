import numpy
from obspy.core import Trace,Stream,UTCDateTime
import Queue
from threading import Thread
import os

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

         	#print sample,timenow

		queue.put(packet)



#this is the worker thread
def save_data():
	while True:
		#print queue.qsize()
		if (queue.qsize()>=block_length):

			#two arrays for reading samples & jitter into
			data=numpy.zeros([block_length],dtype=numpy.int16)
			jitter=numpy.zeros([block_length],dtype=numpy.int16)

			firsttime=True
			totaltime=0
			sample_time = 0
			sample_difference = 0
			
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
			stats = {'network': 'UK', 'station': 'PHYS', 'location': '00',
					'channel': 'BHZ', 'npts': block_length, 'sampling_rate': avg_samplingrate, 
					'mseed': {'dataquality': 'D'},'starttime': starttime}
			
			sample =Stream([Trace(data=data, header=stats)])
      			jitter =Stream([Trace(data=jitter)])

			MseedExist = False
			JitterExist = False

			#write sample data 
    			for File in os.listdir(mseed_directory):
				if File == (str(UTCDateTime().date) + '.mseed'):
					MseedExist = True
            				total_stream = read(mseed_directory+'/'+File)

					for i in range (total_stream.count()):	
						total_stream[i].data = total_stream[i].data.astype(numpy.int16)
					
					total_stream += sample
					total_stream.write(mseed_directory +'/'+ File,format='MSEED',encoding=1,reclen=512)
			
			if MseedExist == False:
				sample.write(mseed_directory +'/'+ str(UTCDateTime().date) + '.mseed',format='MSEED',encoding=1,reclen=512)

			#write jitter data 
    			for File in os.listdir(jitter_directory):
				if File == (str(UTCDateTime().date) + '.mseed'):
					JitterExist = True
            				total_stream = read(jitter_directory+'/'+File)
					
					for i in range (total_stream.count()):	
						total_stream[i].data = total_stream[i].data.astype(numpy.int16)
					
					total_stream += jitter
					total_stream.write(jitter_directory +'/'+ File,format='MSEED',encoding=1,reclen=512)
			
			if JitterExist == False:
				jitter.write(jitter_directory +'/'+ str(UTCDateTime().date) + '.mseed',format='MSEED',encoding=1,reclen=512)



worker_sample = Thread(target=save_data)
worker_sample.start()

read_data()
