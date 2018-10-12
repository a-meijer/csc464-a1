'''
NAME: producers-consumers.py
AUTHOR: Andrew Meijer V00805554
'''
#!/usr/bin/python3
import queue
import threading
import time
import os
import psutil

class female (threading.Thread):
    def run(self):
        womanSwitch.acquire()
        global womanCounter
        womanCounter = womanCounter + 1
        if womanCounter == 1:
            empty.acquire() # first in locks
        womanSwitch.release()

        ladyPlex.acquire()
        print("A woman uses the bathroom.")
        time.sleep(10)
        ladyPlex.release()

        womanSwitch.acquire()
        womanCounter = womanCounter - 1
        if womanCounter == 0:
            empty.release() # last out unlocks
        womanSwitch.release()

class male (threading.Thread):
    def run(self):
        manSwitch.acquire()
        global manCounter
        manCounter = manCounter + 1
        if manCounter == 1:
            empty.acquire() # first in locks
        manSwitch.release()

        gentPlex.acquire()
        print("A man uses the bathroom.")
        time.sleep(3)
        gentPlex.release()

        manSwitch.acquire()
        manCounter = manCounter - 1
        if manCounter == 0:
            empty.release() # last out unlocks
        manSwitch.release()

# Main
empty = threading.Lock()
manSwitch = threading.Lock()
manCounter = 0
womanSwitch = threading.Lock()
womanCounter = 0
gentPlex = threading.Semaphore(3)
ladyPlex = threading.Semaphore(3)

# Create the human beings that must deploy upon the lavatory, as threads.
m1 = male()
m2 = male()
m3 = male()
m4 = male()
w1 = female()
w2 = female()
w3 = female()
w4 = female()

# there are a few different ways to test this
# adding the sleep times (above) showcases the multiplex.
m1.start()
w1.start()
m2.start()
w2.start()
m3.start()
w3.start()
m4.start()
w4.start()
m1.join()
m2.join()
m3.join()
m4.join()
w1.join()
w2.join()
w3.join()
w4.join()
print("All users have completed their bathtimes.")
# memory usage report:
# nts this is not counted in the comprehensibility measurements
pid = os.getpid()
ps = psutil.Process(pid)
mr = ps.memory_info()
print("Bytes used: ", mr.rss)
