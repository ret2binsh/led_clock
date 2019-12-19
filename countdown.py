#!/usr/bin/python
import argparse
import led
import sys
from signal import signal,SIGINT

def interrupt_handler(sig, frame):
    led.cleanup_leds()
    sys.exit(0)

def init_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=int,
            default=3, help="Minutes.")
    parser.add_argument("-s", type=int,
            default=0, help="Seconds")
    return parser.parse_args()

if __name__ == "__main__":

    signal(SIGINT,interrupt_handler)
    arg = init_arg()
    led.init_leds()
    led.countdown(arg.m,arg.s)
    led.cleanup_leds()
