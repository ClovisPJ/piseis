#	print_adc_readings.py - 12/9/2013. Written by David Purdie as part of the openlabtools initiative
#   Uses the adafruit python libraries to sample the ADS1115 at a user defined sampling frequency

from Adafruit_ADS1x15 import ADS1x15
import time
import numpy as np

pga = 4096					# Set full-scale range of programable gain amplifier (page 13 of data sheet), change depending on the input voltage range
ADS1115 = 0x01				# Specify that the device being used is the ADS1115, for the ADS1015 used 0x00
adc = ADS1x15(ic=ADS1115)	# Create instance of the class ADS1x15 called adc

# Function to print sampled values to the terminal
def logdata():
	
	print "sps value should be one of: 8, 16, 32, 64, 128, 250, 475, 860, otherwise the value will default to 250"
		
	frequency = input("Input sampling frequency (Hz):     ")	# Get sampling frequency from user
	sps = input("Input sps (Hz) :     ")						# Get ads1115 sps value from the user
	time1 = input("Input sample time (seconds):     ")			# Get how long to sample for from the user
	
	period = 1.0 / frequency		# Calculate sampling period

	datapoints = int(time1*frequency)		# Datapoints is the total number of samples to take, which must be an integer

	startTime=time.time()					# Time of first sample
	t1=startTime							# T1 is last sample time
	t2=t1									# T2 is current time
	
	for x in range (0,datapoints) :		# Loop in which data is sampled

			while (t2-t1 < period) :		# Check if t2-t1 is less then sample period, if it is then update t2
				t2=time.time()				# and check again		
			t1+=period						# Update last sample time by the sampling period
				
			#print adc.readADCSingleEnded(0, pga, sps), "0mV		", ("%.2f" % (t2-startTime)) , "s"		# Print sampled value and time to the terminal
                       # print adc.readADCSingleEnded(1, pga, sps), "1mV"
                        print adc.readADCSingleEnded(2, pga, sps), "2mV"
                        print adc.readADCSingleEnded(3, pga, sps), "3mV"
                        print adc.readADCDifferential23(256, sps)*1000
# Call to logdata function
logdata()

	
	
	


