'''
NAME: producers-consumers.py
AUTHOR: Andrew Meijer V00805554
In this implementation of Producer-consumer
I use the python Condition class found here:
https://docs.python.org/2/library/threading.html#condition-objects

'''

import threading
import asyncio
import random

# Global Variables
q = []
cv = asyncio.Condition()

# Pseudocode for Producer from Textbook:
# 1 event = waitForEvent()  - "select a random number"
# 2 mutex.wait()            - "enter critical section"
# 3 buffer.add(event)       - "produce the random number"
# 4 items.signal()          - "new item is on queue"
# 5 mutex.signal()          - "exit critical section"
def producer():
    nums = range(100)
    num = random.choice(nums)
    with cv:
        q.append(num)
        cv.notify()
    return

# Pseudocode for Consumer from Textbook:
# 1 items.wait()            -
# 2 mutex.wait()            -
# 3 event = buffer.get()    -
# 4 mutex.signal()          -
# 5 event.process()         -
def consumer():
    with cv:
        while not q:
            cv.wait()
        num = q.pop(0)
    print(num)
    return




#!/usr/bin/python3

import threading
import time

exitFlag = 0
q = []

class producer (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      print_time(self.name, self.counter, 5)
      print ("Exiting " + self.name)

class consumer (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):


# Create new threads
prod = myThread(1, "Thread-1", 1)
cons = myThread(2, "Thread-2", 2)

# Start new Threads
prod.start()
cons.start()
prod.join()
cons.join()
print ("Exiting Main Thread")
