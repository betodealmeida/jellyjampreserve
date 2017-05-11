# JellyJamPreserve

JellyJamPreserve is a Raspberry Pi project that uses the [Jack Timemachine](http://plugin.org.uk/timemachine/) to record audio on the toggle of a switch. It continuously records audio into a 5 minute circular buffer, and when the switch is turned on the buffer is dumped to a file and it starts recording audio to the file until the switch is turned off. This way you can preserve any cool improvisations by recording **sounds from the past**!

In other words, if you turn the switch on at 1:05 pm and turn it off at 1:30 pm you will have an audio file with a recording from 1:00 pm to 1:30 pm. If you come up with an amazing riff while playing your guitar just turn on the switch and keep playing.

![The JellyJamPreserve](https://raw.githubusercontent.com/robertodealmeida/jellyjampreserve/master/images/jellyjampreserve.jpg)

## Requirements

- **A Raspberry Pi**. Any Raspberry Pi should work. I use a Pi 1 Model B because I had a few of them unused at home.
- **An SD card**. The files are recorded as WAV, and take approximately 20 MB per minute. I use a 32 GB SD card.
- **A USB sound card**. We need a way to capture sound. Any cheap USB soundcard should work, just make sure it has a stereo input. I use [this one](https://www.amazon.com/Behringer-U-Control-Ultra-Low-Interface-Software/dp/B0023BYDHK/ref=pd_cp_267_1?_encoding=UTF8&pd_rd_i=B0023BYDHK&pd_rd_r=75GMM5E61DTF7X07XWVM&pd_rd_w=oyXT9&pd_rd_wg=4cPAX&psc=1&refRID=75GMM5E61DTF7X07XWVM).
- **A WiFi card**. This will allow you to get the files with the recordings from the Pi. Remember that some models of the Pi already have WiFi (the 3 and the Zero W, as of this writing).
- **A switch**, to start/stop recording.
- **An LED**, to indicate when the JellyJamPreserve is recording. Because LEDs are cool.

## Pre-built image

The easiest way to use JellyJamPreserve is to download the pre-built image:

1. Download the file [jellyjampreserve.zip](https://www.amazon.com/clouddrive/share/uGG1XANRI8ByEDcit4V7DIRlXFjQkRCkqQaHtzuCr3K?ref_=cd_ph_share_link_copy).
2. Unzip the file.
3. [Write the image](https://www.raspberrypi.org/documentation/installation/installing-images/) `jellyjampreserve.img` to an SD card.
4. Insert the SD card into a computer and edit the file `wpa_supplicant.conf` with your WiFi credentials.
5. Put the card in a Raspberry Pi and turn it on.
6. Log in to the Pi and expand the filesystem ([instructions](#expand-filesystem)).

Now proceed to the [Wire it up](#wire-it-up) section.

## Manual installation

### Install Raspbian

[Install Raspbian](https://www.google.com/search?q=install+raspbian) and make sure you can log into the Raspberry Pi. The instructions below are for Raspbian Jessie.

### Expand filesystem

    $ sudo raspi-config
    -> 7 Advanced Options [enter]
    -> A1 Expand Filesystem [enter]

### Change default sound card

Create the file `/etc/modprobe.d/alsa-base.conf` and add:

    # This sets the index value of the cards but doesn't reorder.
    options snd_usb_audio index=0   
    options snd_bcm2835 index=1

    # Does the reordering.
    options snd slots=snd_usb_audio,snd_bcm2835
    
You can verify the order using the `aplay` command. After a reboot the USB card should appear as card 0:

    $ aplay -l
    **** List of PLAYBACK Hardware Devices ****
    card 0: Device [C-Media USB Audio Device], device 0: USB Audio [USB Audio]
      Subdevices: 1/1
      Subdevice #0: subdevice #0
    ...
    
[Read more here](https://raspberrypi.stackexchange.com/questions/40831/how-do-i-configure-my-sound-for-jasper-on-raspbian-jessie).

### Install jackd2

We need to compile jackd2 from scratch without d-bus support:

    $ sudo apt-get update
    $ sudo apt-get install git build-essential alsa-base libasound2-dev libsamplerate0-dev libsndfile1-dev libreadline-dev
    $ git clone git://github.com/jackaudio/jack2 --depth 1
    $ cd jack2
    $ ./waf configure --alsa
    $ ./waf build
    $ sudo ./waf install
    $ sudo ldconfig
    $ cd ..
    $ rm -rf jack2
    
Edit the file `/etc/security/limits.conf` and add at the bottom:

    @audio - memlock 256000
    @audio - rtprio 75

Log out and log in again.

### Install Timemachine

    $ sudo apt-get install automake autoconf liblo-dev libgtk2.0-dev tmux
    $ git clone https://github.com/swh/timemachine.git
    $ cd timemachine
    $ ./autogen.sh LIBS="-lm" --disable-lash
    $ make
    $ sudo make install
    $ cd ..
    $ rm -rf timemachine

### Create `/dev/gpiomem`

    $ sudo apt-get install rpi-update
    $ sudo rpi-update

### Install Python and dependencies

    $ sudo apt-get install python3 python3-pip
    $ sudo pip3 install python-osc
    $ sudo pip3 install RPi.GPIO

### Install the JellyJamPreserve script

    $ git clone https://github.com/robertodealmeida/jellyjampreserve.git
    
And to have it start at boot:

    $ crontab -e
    
By adding this line:

    @reboot /home/pi/jellyjampreserve/start.sh >> /home/pi/jellyjampreserve.log 2>&1
    
The script will start the Jack daemon, Timemachine, and a Python script that listens for events from the switch and starts/stops Timemachine.

## Wire it up

1. The LED is connected to GPIO 3 (pin 5) and to ground with a 47R resistor.
2. GPIO 2 (pin 3) has a 10K pull-up resistor, and is connected to the ground through the switch.

![Fritzing diagram](https://raw.githubusercontent.com/robertodealmeida/jellyjampreserve/master/images/fritzing.png)

Here's how I did it, slightly different from the Fritzing diagram:

![Connecting the switch and the LED](https://raw.githubusercontent.com/robertodealmeida/jellyjampreserve/master/images/wiring.jpg)

- White wire: LED anode to GPIO 3 (pin 5)
- Black wire: switch to ground (pin 6)
- Yellow wire: switch to GPIO 2 (pin 3)
- Red wire: 10K resistor to 5V (pin 4)

## Getting the files

There are many ways to get the recordings from the Pi. You can have Dropbox or [Syncthing](https://syncthing.net/) running in the Pi to automatically synchronize the files with another machine. I prefer to just use `scp` in Linux (in Windows you can use [WinSCP](https://winscp.net/eng/index.php)).

The Pi is available at the address `jellyjampreserve.local`, and you can log in as user `pi`, password `raspberry`. All the recordings are stored in the directory `/home/pi/recordings/` with an ISO 8601 timestamp of when the recording started (ie, 5 minutes before the switch was toggled).
