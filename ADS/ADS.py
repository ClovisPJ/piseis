#from save_adc_readings import logdata
from obspy.core import read, Trace, Stream, UTCDateTime
import numpy as np
from Adafruit_ADS1x15 import ADS1x15
import time

def logdata():
	ADS1115 = 0x01
	pga = 6144
	adc = ADS1x15(ic=ADS1115)

	print "sps value should be one of: 8, 16, 32, 64, 128, 250, 475, 860, otherwise the value will default to 250"
		
	frequency = input("Input sampling frequency (Hz):     ")	# Get sampling frequency from user
	sps = input("Input sps (Hz) :     ")						# Get ads1115 sps value from the user
	time1 = input("Input sample time (seconds):     ")			# Get how long to sample for from the user
	
	period = 1.0 / frequency		# Calculate sampling period

	datapoints = int(time1*frequency)		# Datapoints is the total number of samples to take, which must be an integer
	dataarray=np.zeros([datapoints,2])		# Create numpy array to store value and time at which samples are taken

	print "Press ENTER to start sampling"
	raw_input()
	
	time.sleep(1)							# Reduces jitter

	startTime=time.time()					# Time of first sample
	t1=startTime							# T1 is last sample time
	t2=t1									# T2 is current time
	
	for x in range (0,datapoints) :			# Loop in which data is sampled
			
			dataarray[x,1] = time.time()-startTime					# Time of sample
			dataarray[x,0]= adc.readADCSingleEnded(0, pga, sps)		# Take a sample

			while (t2-t1 < period) :		# Check if t2-t1 is less then sample period, if it is then update t2
				t2=time.time()				# and check again		
			t1+=period						# Update last sample time by the sampling period
					
	return (dataarray)

#miseedarray=read()

#get data from adc using function
adcereadings=logdata()

print(adcereadings)
#miseedarray.data=adcereadings

# Fill header attributes
stats = {'network': 'BW', 'station': 'RJOB', 'location': '',
         'channel': 'WLZ', 'npts': len(adcereadings), 'sampling_rate': 0.1,
         'mseed': {'dataquality': 'D'}}

stats['starttime'] = UTCDateTime()

#plot = Stream([Trace(data=mseedarray, header=stats)])

miseedarray.plot()

#plot.plot(type='dayplot')
