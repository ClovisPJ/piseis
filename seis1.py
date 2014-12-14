# a first script to print what is coming from the digitser
#  we need to import an external library to read the data 

f input_type == 'A':

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

#  this looprints all the data appearing on this port 

while(port.isOpen()):
    sample = port.readline().strip()
    print sample
