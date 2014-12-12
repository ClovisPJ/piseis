from obspy.core import read
import os
checkedfiles = []
def plotDirectory (directory, previousfiles):
    isfirst = 1 
    for f in os.listdir(directory):
	
        alreadychecked = False
        for fil in previousfiles:
            if f == fil:
                alreadychecked = True
        if not alreadychecked and f.endswith('.mseed') and isfirst == 1:
            totalstream = read(directory+'/'+f)
            previousfiles += f
	    isfirst+=1
        elif not alreadychecked and f.endswith('.mseed'):
            stream = read(directory+'/'+f)
            totalstream += stream
            previousfiles += f
	    isfirst += 1
    totalstream.plot()

plotDirectory("mseed",checkedfiles)
