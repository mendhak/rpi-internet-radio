import datetime
import pytz
import icalendar
import urllib2
from icalendar import Calendar, Event
import ConfigParser

#Read ICS URL from config fie
Config = ConfigParser.ConfigParser()
Config.read("alarm.cfg")
gcalurl = Config.get("default", "GoogleCalendarICSUrl")
gcalkeyword = Config.get("default", "GoogleCalendarEventKeyword")

#Parse ICAL data
response = urllib2.urlopen(gcalurl)
cal = Calendar.from_ical(response.read())

#Find the next event in the next hour
for event in cal.walk('vevent'):
   if (type(event.get('dtstart').dt) is datetime.datetime 
       and event.get('dtstart').dt > pytz.UTC.localize(datetime.datetime.now())):
        timediff = (event.get('dtstart').dt - pytz.UTC.localize(datetime.datetime.now())).total_seconds()
        if timediff < 3600 and gcalkeyword in event.get('summary'):
            print event.get('dtstart').dt, "to", event.get('dtend').dt
            print event.get('summary')
