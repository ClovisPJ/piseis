from Queue import Queue
from threading import Thread
import time

i=1
q = Queue()

def getdata():
	while True:
		print 'getting data'
		time.sleep(2)
		if not q.empty():		
			i = q.get()
			print i
			print 'got data'
			q.task_done()
		else:
			print 'empty!'
			break	

		



for x in range(1):
	worker = Thread(target=getdata)
	#worker.Daemon = True
	worker.start()

for y in range(5):
	q.put(y)


#print 'starting...'
#q.join()
#print 'done!'
