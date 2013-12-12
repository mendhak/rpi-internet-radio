import os
import sys

if os.getuid() != 0:
    sys.exit("You must run this as sudo python alarm.py")

import time
import threading
import signal
import struct
import evdev
import select
import random
import pygame
import math
import array
import fcntl
import datetime
import pytz
import urllib2
import icalendar
from icalendar import Calendar, Event
import ConfigParser



#Read ICS URL from config fie
Config = ConfigParser.ConfigParser()
Config.read("alarm.cfg")
gcalurl = Config.get("default", "GoogleCalendarICSUrl")
gcalkeyword = Config.get("default", "GoogleCalendarEventKeyword")
nextAlarmStart = None
nextAlarmEnd = None

if not os.path.exists("/dev/input/event0"):
    print("WARNING: Touchscreen input at /dev/input/event0 does not exist")

if not os.path.exists("/dev/fb1"):
    sys.exit("FATAL: Can't find PI32 LCD screen! Exiting...")


os.environ['SDL_VIDEODRIVER']="fbcon"
os.environ["FRAMEBUFFER"]="/dev/fb1"
os.environ["SDL_FBDEV"] = "/dev/fb1"

class DisplayThread(threading.Thread):

    def __init__(self):
        print("Display starting...")
        super(DisplayThread, self).__init__()
        self.keepRunning = True

    def run(self):
        pygame.init()
        pygame.font.init()

        ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.mouse.set_visible(False)
        SmallFont = pygame.font.Font(None, 25)
        LargeFont = pygame.font.Font(None,180)

        Background = ThisSurface.copy()

        while self.keepRunning:
            TextReady = LargeFont.render(time.strftime("%S"), True, (0x00, 0xFF, 0x00))
            textrect = TextReady.get_rect()
            textrect.centerx = ThisSurface.get_rect().centerx
            textrect.centery = ThisSurface.get_rect().centery

            # Set background color
            ThisSurface.fill((0x00, 0x00, 0x00))

            # Write some text
            ThisSurface.blit(TextReady, textrect)

            # Render
            pygame.display.flip()
            time.sleep(1)

    def die(self):
        print("Display stopping...")
        self.keepRunning = False



class CalendarThread(threading.Thread):

    def __init__(self, callback):
        self.callback = callback
        self.lastRunTime = None
        self.keepRunning = True
        super(CalendarThread, self).__init__()

    def run(self):
        while self.keepRunning:
            try:
                if self.lastRunTime and (datetime.datetime.now() - self.lastRunTime).total_seconds() < 300:
                    print("Skipping cal loop")
                    continue

	        #Parse ICAL data
                response = urllib2.urlopen(gcalurl)
	        cal = icalendar.Calendar.from_ical(response.read())

                #Find the next event in the next hour
                for event in cal.walk('vevent'):
                    if (type(event.get('dtstart').dt) is datetime.datetime
                     and event.get('dtstart').dt > pytz.UTC.localize(datetime.datetime.now())):
                        timediff = (event.get('dtstart').dt - pytz.UTC.localize(datetime.datetime.now())).total_seconds()
                        if timediff < 3600 and gcalkeyword in event.get('summary'):
                            print event.get('dtstart').dt, "to", event.get('dtend').dt
                            print event.get('summary')
                            self.callback(event.get('dtstart').dt, event.get('dtend').dt)

                self.lastRunTime = datetime.datetime.now()

            except Exception as e:
                print sys.exc_info()[0]
                print e
            finally:
                time.sleep(5)

    def die(self):
        print("Calendar stopping...")
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
        print("Touchscreen stopping...")
        self.keepRunning = False


def stop(signum=None, frame=None):
    print("Stopping all threads")
    ds.die()
    ts.die()
    cal.die()
    sys.exit()



signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

def cb_newAlarm(startDate, endDate):
    global nextAlarmStart
    global nextAlarmEnd
    nextAlarmStart = startDate
    nextAlarmEnd = endDate


print("Starting threads")
ds = DisplayThread()
ts = Touchscreen()
cal = CalendarThread(cb_newAlarm)
ds.start()
ts.start()
cal.start()


try:
    while True:
        if nextAlarmStart:
            if (nextAlarmStart-pytz.UTC.localize(datetime.datetime.now())).total_seconds() < 5:
                print("ALARM GO!", nextAlarmEnd)
                nextAlarmStart = None
                nextAlarmEnd = None
        time.sleep(1)
except:
    print("Exiting threads, please wait...")
    stop()


