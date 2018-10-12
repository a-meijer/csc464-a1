'''
NAME: producers-consumers.py
AUTHOR: Andrew Meijer V00805554
This program is based on the threading code found here:
https://www.tutorialspoint.com/python3/python_multithreading.htm

'''
#!/usr/bin/python3
import queue
import threading
import time
import os
import psutil

class hacker (threading.Thread):
    def run(self):
        print("A hacker boards the boat.")
        global crossing
        global hb
        hb = hb + 1
        crossing = True

class serf (threading.Thread):
    def run(self):
        print("A serf boards the boat.")
        global crossing
        global sb
        sb = sb + 1
        crossing = True

def hackerArrives():
    global hackers
    global serfs
    hackers = hackers + 1
    if(hackers == 4):
        hackers = 0
        hackerQ.get().start()
        hackerQ.get().start()
        hackerQ.get().start()
        hackerQ.get().start()
    elif(hackers == 2 and serfs >= 2):
        hackers = 0
        serfs = serfs - 2
        hackerQ.get().start()
        hackerQ.get().start()
        serfQ.get().start()
        serfQ.get().start()

def serfArrives():
    global hackers
    global serfs
    serfs = serfs + 1
    if(serfs == 4):
        serfs = 0
        serfQ.get().start()
        serfQ.get().start()
        serfQ.get().start()
        serfQ.get().start()
    elif(hackers >= 2 and serfs == 2):
        serfs = 0
        hackers = hackers - 2
        hackerQ.get().start()
        hackerQ.get().start()
        serfQ.get().start()
        serfQ.get().start()

# Main
mutex = threading.Lock()
barrier = threading.Barrier(4)
hackerQ = queue.Queue(10)
serfQ = queue.Queue(10)
hackers = 0
serfs = 0
# hackers boarded
hb = 0
# slaves boarded
sb = 0
crossing = False

# Create new threads
h1 = hacker()
h2 = hacker()
h3 = hacker()
h4 = hacker()
s1 = serf()
s2 = serf()
s3 = serf()
s4 = serf()

# Add threads to queue
hackerQ.put(h1)
hackerQ.put(h2)
hackerQ.put(h3)
hackerQ.put(h4)
serfQ.put(s1)
serfQ.put(s2)
serfQ.put(s3)
serfQ.put(s4)

# TESTING WITH VARIOUS PASSENGERS:
serfArrives()
serfArrives()
serfArrives()
serfArrives()

# wait until everyone has their go.
s1.join()
s2.join()
s3.join()
s4.join()

if crossing:
    print ("The rowboat crosses the river with", sb, " serfs and ", hb, " hackers.")
else:
    print ("Incorrect passengers to cross the river.")
# memory usage report:
# nts this is not counted in the comprehensibility measurements
pid = os.getpid()
ps = psutil.Process(pid)
mr = ps.memory_info()
print("Bytes used: ", mr.rss)
