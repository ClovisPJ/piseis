# a first script to print what is coming from the digitser
#  we need to import an external library to read the data 
import serial


# the original SEP serial port digitser appers as devive /dev/ttyUSB0
# the new SEP USB digitiser appears as device /dev/ttyACMO
#port_name = '/dev/ttyACM0'
port_name = '/dev/ttyUSB0'

port = serial.Serial(port_name, 9600, timeout=1)

#  this looprints all the data appearing on this port 

while(port.isOpen()):
    sample = port.readline().strip()
    print sample