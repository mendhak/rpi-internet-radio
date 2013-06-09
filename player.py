import RPi.GPIO as GPIO
import time
import sys
import commands

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(11, GPIO.OUT)
prev1 = 0

def SetLEDStatus(oNOff):
    GPIO.output(11, oNOff)

def BlinkIndicateOn():
    SetLEDStatus(True)
    time.sleep(0.5)
    SetLEDStatus(False)
    time.sleep(0.5)
    SetLEDStatus(True)
    time.sleep(0.5)
    SetLEDStatus(False)

BlinkIndicateOn()


try:
    while True:
        if ( GPIO.input(16) == False ):
            prev1 += 1
        if ( prev1 > 0 and GPIO.input(16) == True ):
            if prev1 < 10:
                print "Next song"
                commands.getstatusoutput("mpc clear")
                print commands.getstatusoutput("mpc lsplaylists | shuf -n 1 | mpc load")[1]
                commands.getstatusoutput("mpc play")
                SetLEDStatus(True)
            else:
                mpc = commands.getstatusoutput("mpc")
                if ( "playing" in mpc[1] ):
                    print "Stopping music"
                    commands.getstatusoutput("mpc stop")
                    SetLEDStatus(False)
                else:
                    print "Starting music"
                    print commands.getstatusoutput("mpc lsplaylists | shuf -n 1 | mpc load")[1]
                    commands.getstatusoutput("mpc play")
                    SetLEDStatus(True)
            prev1 = 0
        if ( GPIO.input(18) == False ):
            mpcvolume = commands.getstatusoutput("mpc volume")
            volume = int(mpcvolume[1].replace("volume:","").replace(" ","").replace("%",""))
            volume -= 1
            commands.getstatusoutput("mpc volume " + str(volume))
            print "Vol down pressed"
        if ( GPIO.input(22) == False ):
            mpcvolume = commands.getstatusoutput("mpc volume")
            volume = int(mpcvolume[1].replace("volume:","").replace(" ","").replace("%",""))
            volume += 1
            commands.getstatusoutput("mpc volume " + str(volume))
            print "Vol up pressed"
        time.sleep(0.1)
except KeyboardInterrupt:
    print "Stopping"
    GPIO.cleanup()
    sys.exit()

