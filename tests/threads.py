import time
import os
import threading

class First(threading.Thread):
    def __init__(self):
        self.keepRunning = True
        super(First, self).__init__()

    def run(self):
        try:
            while self.keepRunning:
                print("First thread")
                time.sleep(3)
        except:
            return

    def die(self):
        self.keepRunning = False



class Second(threading.Thread):
    def __init__(self):          
        self.keepRunning = True
        super(Second, self).__init__()

    def run(self):
        try:
            while self.keepRunning:
                print("Second thread")
                time.sleep(6)
        except:
            return 

    def die(self):
        self.keepRunning = False


print("Starting threads")
f = First()
s = Second()
f.start()
s.start()

try:
    while True:
        time.sleep(20)
except:
    print("Exiting threads, please wait...")
    f.die()
    s.die()


