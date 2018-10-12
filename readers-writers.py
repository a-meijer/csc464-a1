'''
NAME: readers-writers.py
AUTHOR: Andrew Meijer V00805554
'''

#!/usr/bin/python3
import threading
import time
import os
import psutil

readers = 0
writing = ""
doneWriting = 0

class writer (threading.Thread):
   def run(self):
      print ("Starting new writer thread.")
      global writing
      w = input("Update the writing: ")

      # ~ critical ~
      roomEmpty.acquire()
      writing = w
      roomEmpty.release()

      print ("Writing is finished.")
      global doneWriting
      doneWriting = 1

class reader (threading.Thread):
    def run(self):
        print ("New reader thread begins.")

        # number of readers in the room is protected
        mutex.acquire()
        global readers
        readers = readers + 1
        if readers == 1:
            roomEmpty.acquire()

        mutex.release()

        # critical section
        print ("There are now ", readers, " readers reading.")
        print('Reader reads "', writing, '" for 2 seconds.')
        time.sleep(2)

        mutex.acquire()
        readers = readers - 1
        if readers == 0:
            roomEmpty.release()
        mutex.release()

# Main
mutex = threading.Lock()
roomEmpty = threading.Lock()

# Create new threads
# Threads can only be started once
r1 = reader()
r2 = reader()
r3 = reader()
w1 = writer()
w2 = writer()

# Start new Threads
# To test readers-writers I will do a few steps:
# Write to shared variable "writing"
# Read with only one reader
# Write again
# Read with 2 readers
w1.start()
r1.start()

# wait
while not doneWriting:
    pass

doneWriting = 0;
w2.start()
r2.start()
r3.start()

# wait until
while not doneWriting:
    pass

print ("Exiting Main Thread.")
# memory usage report:
# nts this is not counted in the comprehensibility measurements
pid = os.getpid()
ps = psutil.Process(pid)
mr = ps.memory_info()
print("Bytes used: ", mr.rss)
