from obspy.core import read
import os
checkedfiles = []
def plotDirectory (directory, previousfiles):
    #totalstream = ''
    isfirst = 0
    isfirst += 1
    for f in os.listdir(directory):
        
        alreadychecked = False
        for fil in previousfiles:
            if f == fil:
                alreadychecked = True
        if not alreadychecked and f.endswith('.mseed') and isfirst == 1:
            totalstream = read(f)
            previousfiles += f
        elif not alreadychecked and f.endswith('.mseed'):
            stream = read(f)
            totalstream += stream
            previousfiles += f
    totalstream.plot()
plotDirectory('/home/pi/OUNDLESEIS/mseed', checkedfiles)

            
