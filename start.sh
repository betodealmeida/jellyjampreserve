#!/bin/bash

# jack server
/usr/local/bin/jackd -R -dalsa -dhw:0 -r48000 -p1024 -n3 &

# timemachine
mkdir -p recordings/
timemachine -i -t 300 -f wav -p recordings/ &

# connections
sleep 5
jack_connect system:capture_1 system:playback_1
jack_connect system:capture_2 system:playback_2
jack_connect system:capture_1 TimeMachine:in_1
jack_connect system:capture_2 TimeMachine:in_2
jack_lsp -c
