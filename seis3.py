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

#number of samples in each mseed file
block_length=128

#iterator for writing files
block_id=0

x=0

#this is needed for saving in mseed so must be passed globably 
global starttime

global block_id

#define the queue from using the library
q = Queue.Queue()


def read_data(block_length):
	starttime=UTCDateTime()
	while x<block_length:
		
		#loop continues for block length
	        sample = read()
		
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



worker = Thread(target=save_data)
worker.start()

for x in range(5):
	read_data(block_length)
