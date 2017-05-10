# JellyJamPreserve

JellyJamPreserve is a Raspberry Pi project that uses the [Jack Timemachine](http://plugin.org.uk/timemachine/) to record audio on the toggle of a switch. It continuously records audio into a 5 minute circular buffer, and when the switch is turned on the buffer is dumped to a file and it starts recording audio to the file until the switch is turned off. This way you can preserve any cool improvisations by recording **sounds from the past**!

In other words, if you turn the switch on at 1:05 pm and turn it off at 1:30 pm you will have an audio file with a recording from 1:00 pm to 1:30 pm. If you come up with an amazing riff while playing your guitar just turn on the switch and keep playing.

## Requirements

- **A Raspberry Pi**. Any Raspberry Pi should work. I use a Pi 1 Model B because I had a few of them unused at home.
- **An SD card**. The files are recorded as WAV, and take approximately 20 MB per minute. I use a 32 GB SD card.
- **A USB sound card**. We need a way to capture sound. Any cheap USB soundcard should work, just make sure it has a stereo input. I use [this one](https://www.amazon.com/Behringer-U-Control-Ultra-Low-Interface-Software/dp/B0023BYDHK/ref=pd_cp_267_1?_encoding=UTF8&pd_rd_i=B0023BYDHK&pd_rd_r=75GMM5E61DTF7X07XWVM&pd_rd_w=oyXT9&pd_rd_wg=4cPAX&psc=1&refRID=75GMM5E61DTF7X07XWVM).
- **A switch**, to start/stop recording.
- **An LED**, to indicate when the JellyJamPreserve is recording. Because LEDs are cool.

## Pre-built image

I'll make a pre-built image available here. In the meantime, follow the manual installation.

## Manual installation

### Install Raspbian

[Install Raspbian](https://www.google.com/search?q=install+raspbian). The instructions here are for Jessie.

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

## Wire it up

1. The LED is connected to GPIO 3 (pin 5) and to ground with a 47R resistor.
2. GPIO 2 (pin 3) has a 10K pull-up resistor, and is connected to the ground through the switch.

![Connecting the switch and the LED](https://raw.githubusercontent.com/robertodealmeida/jellyjampreserve/master/wiring.png)
