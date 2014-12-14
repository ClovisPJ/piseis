import numpy
from obspy.core import Trace,Stream,UTCDateTime
import Queue
from threading import Thread

if input_type == 'A':

        from Adafruit_ADS1x15 import ADS1x15
        sps = 16        #samples per second
        #pga = 4096     #programmable gain amplifier
        adc = ADS1x15(ic=0x01)  #create class identifing model used

        def read():
                return adc.readADCDifferential23(256, sps)*1000
elif input_type == 'D':

        import serial
        port_name = '/dev/ttyACM0'
        port = serial.Serial(port_name, 9600, timeout=1)

        def read():
                return port.readline().strip()
else:
        sys.exit("Incorrect ADS type")

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

	       	sample = read()

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
			
			st =Stream([Trace(data=data, header=stats)])
      			jt =Stream([Trace(data=jitter)])
			
			#write block with id from iterator
			st.write('mseed/PHYS' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			jt.write('mseed/JTR' + str(block_id) + '.mseed',format='MSEED',encoding='INT16',reclen=512)
			block_id=block_id+1




worker_sample = Thread(target=save_data)
worker_sample.start()

for x in range (5):
	read_data(block_length)
