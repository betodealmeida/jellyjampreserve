#!/bin/bash

# echo commands
set -x
date

# start the jack server
echo "Starting JACK server"
/usr/local/bin/jackd -R -dalsa -dhw:0 -r48000 -p1024 -n3 &

# run timemachine in tmux, since it waits for input
mkdir -p /home/pi/recordings/
sleep 5
echo "Starting Timemachine"
tmux new-session -d '/usr/local/bin/timemachine -i -t 300 -f wav -p /home/pi/recordings/ system:capture_1 system:capture_2'

# connections
echo "Connecting system capture to playback"
/usr/local/bin/jack_connect system:capture_1 system:playback_1
/usr/local/bin/jack_connect system:capture_2 system:playback_2
/usr/local/bin/jack_lsp -c

echo "Starting JellyJamPreserve"
python3 /home/pi/jellyjampreserve/jellyjampreserve.py &
