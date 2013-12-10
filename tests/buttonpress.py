#!/usr/bin/env python
import time, sys
import fcntl, array

x = 1
file = open("/dev/fb1")
buf = array.array('h', [0])

while True:
    try:
        
        x = fcntl.ioctl(file, -444763391, buf, 1)
        #print x
        if buf[0] != 31:
            print buf[0]
        time.sleep(.3)
    except KeyboardInterrupt:
        print "Bye"
        sys.exit()
