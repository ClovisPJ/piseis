from obspy.core import read,UTCDateTime
import os.path
import os

previous_size = 0

File = 'mseed/' + UTCDateTime().date + '.mseed'

While True:
       If os.path.exists(File):
               If os.path.getsize(File) != previous_size
                       plot(File)
               Elif Date != UTCDateTime().date:
                       Date = UTCDateTime()
                       plot(File)


def plot(filename):
       stream.read(filename)
       #kill osbpy server
       stream.plot()
       previous_size=os.path.getsize(filename)

