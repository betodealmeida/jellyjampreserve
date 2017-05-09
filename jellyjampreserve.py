#!/usr/bin/python3

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient
import RPIO


HOST = '127.0.0.1'
PORT = 7133
SWITCH = 3  # 10K pull up resistor and switch to ground
LED = 5     # 47R resistor to ground

RPIO.setmode(RPIO.BOARD)
RPIO.setup(LED, RPIO.OUT, initial=RPIO.LOW)


def record(gpio_id, value):
    client = UDPClient(HOST, PORT)
    msg = OscMessageBuilder('/start').build()
    client.send(msg)
    RPIO.output(LED, True)


def stop(gpio_id, value):
    client = UDPClient(HOST, PORT)
    msg = OscMessageBuilder('/stop').build()
    client.send(msg)
    RPIO.output(LED, False)


def main():
    RPIO.add_interrupt_callback(SWITCH, record, edge='rising',
                                debounce_timeout_ms=10)
    RPIO.add_interrupt_callback(SWITCH, stop, edge='falling',
                                debounce_timeout_ms=10)
    RPIO.wait_for_interrupts()


if __name__ == '__main__':
    main()
