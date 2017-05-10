#!/bin/bash

# jack server
echo "Starting JACK server"
/usr/local/bin/jackd -R -dalsa -dhw:0 -r48000 -p1024 -n3 &

# timemachine
mkdir -p /home/pi/recordings/
echo "Starting Timemachine"
timemachine -i -t 300 -f wav -p /home/pi/recordings/ &

# connections
echo "Waiting before setting up connections..."
sleep 5
echo "Connecting system capture to playback"
jack_connect system:capture_1 system:playback_1
jack_connect system:capture_2 system:playback_2
echo "Connecting system capture to Timemachine"
jack_connect system:capture_1 TimeMachine:in_1
jack_connect system:capture_2 TimeMachine:in_2
echo "All connections ready"
jack_lsp -c

echo "Starting JellyJamPreserver"
python3 /home/pi/jellyjampreserve/jellyjampreserve.py &
