import time
import os
import threading
import signal
import sys
import struct
import evdev
import select


class Calendar(threading.Thread):
    def __init__(self):
        self.keepRunning = True
        super(Calendar, self).__init__()

    def run(self):
        try:
            while self.keepRunning:
                print("First thread")
                time.sleep(3)
        except:
            return

    def die(self):
        self.keepRunning = False



class Touchscreen(threading.Thread):
    def __init__(self):          
        #long int, long int, unsigned short, unsigned short, unsigned int
        self.FORMAT = 'llHHI'
        self.EVENT_SIZE = struct.calcsize(self.FORMAT)
        #open file in binary mode
        self.keepRunning = True
        super(Touchscreen, self).__init__()

    def run(self):
        dev = evdev.InputDevice("/dev/input/event0")
        while self.keepRunning:
            r,w,x = select.select([dev.fd], [], [], 0.1)
            if r:
                for event in dev.read():
                    print(event)

    def die(self):
        self.keepRunning = False


def stop(signum=None, frame=None):
    ts.die()
    cal.die()
    sys.exit()



signal.signal(signal.SIGTERM, stop)


print("Starting threads")
ts = Touchscreen()
cal = Calendar()
ts.start()
cal.start()


try:
    while True:
        print("Main thread")
        time.sleep(20)
except:
    print("Exiting threads, please wait...")
    stop()


