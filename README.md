# JellyJamPreserve

JellyJamPreserve is a Raspberry Pi project that uses the [Jack Timemachine](http://plugin.org.uk/timemachine/) to record audio on the click of button (or toggle of a switch). It continuously records audio into a 5 minute circular buffer, and when the button is clicked the buffer is dumped to a file and it starts recording audio to the file until the button is clicked again. This way you can preserve any cool improvisations by recording **sounds from the past**!

## Pre-built image

## Manual installation

### Install Raspbian

### Change default sound card

Edit the file `/etc/modprobe.d/alsa-base.conf` and change:

    #options snd-usb-audio index=-2
    options snd-usb-audio index=0

Also edit `~/.asoundrc`:

    pcm.!default {
        type hw
        card 0
    }
    
    ctl.!default {
        type hw
        card 0
    }

### Expand filesystem

    sudo raspi-config

### Install jackd2

    git clone git://github.com/jackaudio/jack2 --depth 1
    cd jack2
    ./waf configure --alsa
    ./waf build
    sudo ./waf install
    sudo ldconfig
    
Edit the file `/etc/security/limits.conf` and add at the bottom:

    @audio - memlock 256000
    @audio - rtprio 75

### Install Timemachine 

### Install Python

## Wire it up
