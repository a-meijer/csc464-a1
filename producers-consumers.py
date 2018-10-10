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

exitFlag = 0
startFlag = 0

# Pseudocode for Producer from Textbook:
# 1 event = waitForEvent()  - "select a random number"
# 2 mutex.wait()            - "enter critical section"
# 3 buffer.add(event)       - "produce the random number"
# 4 mutex.signal()          - "exit critical section"
# 5 items.signal()          - "new item is on queue"
class producer (threading.Thread):
   def run(self):
      print ("Starting producer thread.")
      num = input("Produce a number: ")
      # this flag keeps the program running until an event occurs
      global startFlag
      startFlag = 1
      mutex.acquire()
      buffer.put(num)
      mutex.release()
      print ("Exiting producer thread.")

# Pseudocode for Consumer from Textbook:
# 1 items.wait()            -
# 2 mutex.wait()            -
# 3 event = buffer.get()    -
# 4 mutex.signal()          -
# 5 event.process()         -
class consumer (threading.Thread):
    def run(self):
        print ("Starting consumer thread.")
        while not exitFlag:
            mutex.acquire()
            if not buffer.empty():
                num = buffer.get()
                mutex.release()
                print("Consumed: ", num)
            else:
                mutex.release()
                # give time for other possible threads
                time.sleep(1)
        print ("Exit flag is called. Consumption is over.")

# Main
mutex = threading.Lock()
buffer = queue.Queue(10)

# Create new threads
prod = producer()
cons = consumer()

# Start new Threads
prod.start()
cons.start()

# wait until queue is empty
# nts: this is perhaps unnecessary with only one consumer
while not buffer.empty() or not startFlag:
    pass

exitFlag = 1

prod.join()
cons.join()
print ("Exiting Main Thread")
