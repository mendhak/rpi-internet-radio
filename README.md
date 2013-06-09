Raspberry Pi Internet Radio
==================

My own implementation of an Internet radio player on a Raspberry Pi with a breadboard. 

##Hardware
Wired up on a breadboard with a few common components. This was done with a Raspberry Pi Model A. 

###Ingredients

* 3x 10K Ω resistors
* 1x 100 Ω resistor
* 1x LED
* 3x momentary push buttons
* 1x breadboard
* 3x male-to-male jumper cables
* 6x male-to-female jumper cables

###Layout

Arrange the components as shown in this professionally drawn schematic

![Google Drawing](https://docs.google.com/drawings/d/1pTASpTHduzxbRdfg-EzTlNQTGg3yXOJpRtLTJLngTbE/pub?w=960&h=720)


###Reference Photo

![Layout](http://farm3.staticflickr.com/2832/8994587405_99730d2fc1_b.jpg)


##Software
This involves an init.d script and a python script which listens for button presses.

###Ingredients

* `mpc` and `mpd` installed
* `python-dev` and `python-rpi.gpio` installed

###Setup


Copy or clone this repository onto your Raspberry pi

    git clone git://github.com/mendhak/rpi-internet-radio.git


Edit the `/etc/mpd.conf` file and set `playlist_directory` to the stations subfolder of the repository

    playlist_directory              "/home/mendhak/rpi-internet-radio/stations"


Set up the init.d service pointing at the radio script

    sudo ln -s /home/mendhak/rpi-internet-radio/radio radio
    sudo chmod 777 /home/mendhak/rpi-internet-radio/radio
    sudo update-rc.d radio defaults
    
Finally, restart the Raspberry Pi

##Usage

When the Raspberry Pi boots up and the init.d script kicks in, the red LED should flash twice.

To **start** playing music, press the first push button.

To move to the **next** radio station, press the first push button again.

To **stop** playing music, hold the first push button for one second, then let go.

Use the other two push buttons to increase and decrease the **volume**.

To set your own stations, edit or create new `m3u` files in the stations subfolder. 
    
