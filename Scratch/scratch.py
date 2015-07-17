#libraries needed
from array import array
import socket
import time
import sys

#this sets the ip and port of the computer running scratch
PORT = 42001
#note if scratch on this computer enter 'localhost'
HOST = raw_input("Please enter IP address")

#sets up connection to scratch
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))

#function to send data through connection to scratch
def sendScratchCommand(cmd):
    #this array contains the length of message in letters, each char num representing 8 bits of length. 'c' at beginning message handler
    #read more about protocol here: http://wiki.scratch.mit.edu/wiki/Remote_Sensors_Protocol
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    #then send message with length
    scratchSock.send(a.tostring() + cmd)

#setup usb adc (mindsets)
import serial
port_name=raw_input("Please enter ADC location [eg /dev/ttyACM0]:") or "/dev/ttyACM0"
port=serial.Serial(port_name,9600,timeout=1)

#setup accelerometer (adxl345)
from adxl345 import ADXL345

while True:
    #takes adc reading and sends it
    sample=port.readline().strip()
    #print sample
    sendScratchCommand('sensor-update' + ' "sample" ' + sample)

    #takes xyz reading and sends as seperate values
    adxl345 = ADXL345()
    #true gives value in g, false in ms^2
    axes = adxl345.getAxes(True)
    x = str(axes['x'])
    y = str(axes['y'])
    z = str(axes['z'])
    #print x,y,z
    sendScratchCommand('sensor-update'+' "x" '+x+' "y" '+y+' "z" '+z)
