#!/usr/bin/python3

import time

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient
import RPi.GPIO as GPIO


HOST = '127.0.0.1'
PORT = 7133
SWITCH = 2
LED = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
GPIO.setup(SWITCH, GPIO.IN)


def callback(gpio_id):
    client = UDPClient(HOST, PORT)
    if GPIO.input(gpio_id) == 0:
        msg = OscMessageBuilder('/start').build()
        GPIO.output(LED, GPIO.HIGH)
    else:
        msg = OscMessageBuilder('/stop').build()
        GPIO.output(LED, GPIO.LOW)
    client.send(msg)


def main():
    GPIO.add_event_detect(SWITCH, GPIO.BOTH, callback=callback, bouncetime=100)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
