#!/usr/bin/python3

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient
import RPIO


HOST = '127.0.0.1'
PORT = 7133
SWITCH = 2
LED = 3

RPIO.setup(LED, RPIO.OUT, initial=RPIO.LOW)


def callback(gpio_id, value):
    client = UDPClient(HOST, PORT)
    if value == 0:
        msg = OscMessageBuilder('/start').build()
        RPIO.output(LED, True)
    else:
        msg = OscMessageBuilder('/stop').build()
        RPIO.output(LED, False)
    client.send(msg)


def main():
    RPIO.add_interrupt_callback(SWITCH, callback, edge='both')
    RPIO.wait_for_interrupts()


if __name__ == '__main__':
    main()
