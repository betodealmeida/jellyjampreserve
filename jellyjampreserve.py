#!/usr/bin/python3

import time

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient
import RPi.GPIO as GPIO


HOST = '127.0.0.1'
PORT = 7777
SWITCH = 2
LED = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
GPIO.setup(SWITCH, GPIO.IN)

START = OscMessageBuilder('/jack_capture/tm/start').build()
STOP = OscMessageBuilder('/jack_capture/tm/stop').build()
client = UDPClient(HOST, PORT)


def callback(gpio_id):
    if GPIO.input(gpio_id) == 0:
        GPIO.output(LED, GPIO.HIGH)
        client.send(START)
    else:
        GPIO.output(LED, GPIO.LOW)
        client.send(STOP)


def main():
    GPIO.add_event_detect(SWITCH, GPIO.BOTH, callback=callback, bouncetime=100)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
