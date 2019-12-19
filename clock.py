#!/usr/bin/python
import led
import time
from signal import signal,SIGINT
from sys import exit


def get_time():
    ts = time.localtime()
    return ts[3],ts[4]

def cntlc_handler(sig, frame):
    led.cleanup_leds()
    exit(0)

if __name__ == "__main__":

    signal(SIGINT,cntlc_handler)

    led.init_leds()

    while True:
        hour,minute = get_time()
        pos1 = led.get_num_index(hour,1)
        pos2 = led.get_num_index(hour,0)
        pos3 = led.get_num_index(minute,1)
        pos4 = led.get_num_index(minute,0)

        for _ in range(333):
            led.display_position(1, pos1, .001)
            led.display_position(2, pos2, .001)
            led.display_position(3, pos3, .001)
            led.display_position(4, pos4, .001)
