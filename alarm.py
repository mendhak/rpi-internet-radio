import os
import sys

# Inital checks
if os.getuid() != 0:
    sys.exit("You must run this as sudo python alarm.py")

if not os.path.exists("/dev/input/event0"):
    print("WARNING: Touchscreen input at /dev/input/event0 does not exist")

if not os.path.exists("/usr/bin/mpc") or not os.path.exists("/usr/bin/mpd"):
    print("FATAL: Please ensure that mpc and mpd are installed.")

if not os.path.exists("/dev/fb1"):
    sys.exit("FATAL: Can't find PI32 LCD screen! Exiting...")


# Set the framebuffer device; /dev/fb1 is the PI32 touchscreen
os.environ['SDL_VIDEODRIVER']="fbcon"
os.environ["FRAMEBUFFER"]="/dev/fb1"
os.environ["SDL_FBDEV"] = "/dev/fb1"


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
import commands



# Initialize values and read config
Config = ConfigParser.ConfigParser()
Config.read("alarm.cfg")
gcalurl = Config.get("default", "GoogleCalendarICSUrl")
gcalkeyword = Config.get("default", "GoogleCalendarEventKeyword")
lastMpcCheck = datetime.datetime.now()
nextAlarmStart = None
nextAlarmEnd = None
nextAlarmMessage = None

class DisplayThread(threading.Thread):

    def __init__(self):
        print("Display starting...")
        super(DisplayThread, self).__init__()
        self.keepRunning = True
        self.currentlyAlarming = False

    def run(self):
        pygame.init()
        pygame.font.init()

        ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.mouse.set_visible(False)
        SmallFont = pygame.font.Font(None, 25)
        LargeFont = pygame.font.Font(None,180)

        Background = ThisSurface.copy()

        while self.keepRunning:
            TextTime = LargeFont.render(time.strftime("%H:%M"), True, (0x00, 0xFF, 0x00))
            textrect = TextTime.get_rect()
            textrect.centerx = ThisSurface.get_rect().centerx
            textrect.centery = ThisSurface.get_rect().centery
            TextSec = SmallFont.render(time.strftime("%S"), True, (0xFF, 0xFF, 0xFF))
            textrect2 = TextSec.get_rect()
            textrect2.topright = textrect.topright
            TextMsg = None

            if self.alarmMessage:
                TextMsg = SmallFont.render(self.alarmMessage, True, (0xFF, 0xFF, 0xFF))
                textmsgrect = TextMsg.get_rect()
                textmsgrect.centerx = ThisSurface.get_rect().centerx
                textmsgrect.top = textrect.bottom

            # Set background color
            if self.currentlyAlarming:
                ThisSurface.fill((0xFF, 0x00, 0x00))
            else:
                ThisSurface.fill((0x00,0x00,0x00))

            # Write some text
            ThisSurface.blit(TextTime, textrect)
            ThisSurface.blit(TextSec, textrect2)

            if TextMsg:
                ThisSurface.blit(TextMsg, textmsgrect)

            # Render
            pygame.display.flip()
            time.sleep(1)


    def alarming(self, status, message=None):
        self.currentlyAlarming = status
        self.alarmMessage = message

    def message(self, message):
        if not self.currentlyAlarming:
            self.alarmMessage = message

    def die(self):
        print("Display stopping...")
        self.keepRunning = False



class CalendarThread(threading.Thread):

    def __init__(self, callback):
        print("Calendar starting...")
        self.callback = callback
        self.lastRunTime = None
        self.keepRunning = True
        super(CalendarThread, self).__init__()

    def run(self):
        while self.keepRunning:
            try:
                if self.lastRunTime and (datetime.datetime.now() - self.lastRunTime).total_seconds() < 300:
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
                            print("Next alarm: {0} from {1} to {2}".format(event.get('summary'), 
                                                       event.get('dtstart').dt, event.get('dtend').dt))
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
    def __init__(self, callback):          
        print("Touchscreen starting...")
        #long int, long int, unsigned short, unsigned short, unsigned int
        self.FORMAT = 'llHHI'
        self.EVENT_SIZE = struct.calcsize(self.FORMAT)
        #open file in binary mode
        self.keepRunning = True
        self.callback = callback
        super(Touchscreen, self).__init__()

    def run(self):
        dev = evdev.InputDevice("/dev/input/event0")
        while self.keepRunning:
            r,s,t = select.select([dev.fd], [], [], 0.1)
            #print r,w,x
            if r:
                for event in dev.read():
                    if event.type == 3:
                        if event.code == 0:
                            x = event.value
                        if event.code == 1:
                            y = event.value
                        if event.code == 24:
                            p = event.value
    
                if x and y and p:
                    self.callback(x,y,p)
                    x = None
                    y = None
                    p = None
                time.sleep(1)

    def die(self):
        print("Touchscreen stopping...")
        self.keepRunning = False

class ButtonThread(threading.Thread):
    def __init__(self, callback):
        print("Buttons starting...")
        super(ButtonThread, self).__init__()
        self.keepRunning = True
        self.callback = callback
   
    def run(self):
        x = 1
        file = open("/dev/fb1")
        buf = array.array('h', [0])

        while self.keepRunning:
            try:
                x = fcntl.ioctl(file, -444763391, buf, 1)
                #print x
                if buf[0] != 31:
                    self.callback(buf[0])
                time.sleep(.3)
            except KeyboardInterrupt:
                return

    def die(self):
        print("Buttons stopping...")
        self.keepRunning = False


def stop(signum=None, frame=None):
    print("Stopping all threads")
    bs.die()
    ds.die()
    ts.die()
    cal.die()
    sys.exit()



signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

def cb_touch(x, y, pressure):
    print("User touched X:{0}, Y:{1}, Pressure:{2}".format(x,y,pressure))
    ds.alarming(False)
    toggleMusic()

def cb_newAlarm(startDate, endDate, message=None):
    global nextAlarmStart
    global nextAlarmEnd
    global nextAlarmMessage
    nextAlarmStart = startDate
    nextAlarmEnd = endDate
    nextAlarmMessage = message

def cb_buttonPress(num):
    if num == 23:
        print("Button: Next station")
        nextMusic()

    if num == 27:
        mpcvolume = commands.getstatusoutput("mpc volume")
        volume = int(mpcvolume[1].replace("volume:","").replace(" ","").replace("%",""))
        volume += 1
        print("Button: Volume up ({0})".format(volume))
        commands.getstatusoutput("mpc volume " + str(volume))

       
    if num == 29:
        mpcvolume = commands.getstatusoutput("mpc volume")
        volume = int(mpcvolume[1].replace("volume:","").replace(" ","").replace("%",""))
        volume -= 1
        print("Button: Volume down ({0})".format(volume))
        commands.getstatusoutput("mpc volume " + str(volume))
    
    if num == 15:
        print("Button: Start/Stop")
        toggleMusic()
    
    if num == 30:
        print("Button 30 does nothing")


def toggleMusic():
    print(commands.getstatusoutput("mpc toggle"))
    showCurrentTrack()

def playMusic():
    print( commands.getstatusoutput("mpc next"))
    print(commands.getstatusoutput("mpc play"))
    showCurrentTrack()

def stopMusic():
    print(commands.getstatusoutput("mpc stop"))
    showCurrentTrack()

def nextMusic():
    print(commands.getstatusoutput("mpc next"))
    showCurrentTrack()

def startAlarm(start, end, message):
    print("START ALARM", message)
    #Set background red
    #Play music
    #Other effects
    playMusic()
    ds.alarming(True, message)

def stopAlarm():
    print("STOP ALARM")
    #Background black?
    stopMusic()
    ds.alarming(False)

def showCurrentTrack():
    if '[playing]' in commands.getstatusoutput("mpc")[1]:
        track = commands.getstatusoutput("mpc current")[1]
        track = track[:25] + (track[25:] and '...')
        ds.message(track)
    else:
        ds.message('')

print("Starting threads")
print(commands.getstatusoutput("mpc clear"))
print(commands.getstatusoutput("mpc lsplaylists | sort --random-sort | mpc load"))
bs = ButtonThread(cb_buttonPress)
ds = DisplayThread()
ts = Touchscreen(cb_touch)
cal = CalendarThread(cb_newAlarm)
bs.start()
ds.start()
ts.start()
cal.start()
ds.alarming(False)

try:
    while True:
        if (datetime.datetime.now() - lastMpcCheck).total_seconds() > 10:
            showCurrentTrack()
            lastMpcCheck = datetime.datetime.now()
        if nextAlarmStart:
            if (nextAlarmStart-pytz.UTC.localize(datetime.datetime.now())).total_seconds() < 2:
                startAlarm(nextAlarmStart, nextAlarmEnd, nextAlarmMessage)
                nextAlarmStart = None

        if nextAlarmEnd:
            if (nextAlarmEnd - pytz.UTC.localize(datetime.datetime.now())).total_seconds() < 2:
                stopAlarm()
                nextAlarmEnd = None
        time.sleep(1)
except:
    stop()


