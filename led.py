import RPi.GPIO as GPIO
import time


'''
Setup Pin to variable associations
LED PINOUT:

    D1     D2     D3     D4
    A
   ---     ---    ---    ---
F |   |B  |   |  |   |  |   |
  | G |   |   |  |   |  |   |
   ---     ---    ---    ---
E |   |C  |   |  |   |  |   |
  |   |   |   |  |   |  |   |
   ---     ---    ---    ---
    D
'''

A,B,C,D,E,F,G = 5,18,36,35,33,7,38
D1,D2,D3,D4   = 3,12,16,40
decimal = 37
led_all = [A,B,C,D,E,F,G,D1,D2,D3,D4,decimal]

'''
Setting the pins to high turns the LED on when position x is
enabled.
'''
led_number = {
        0: {GPIO.HIGH: [A,B,C,D,E,F],   GPIO.LOW: [G]},
        1: {GPIO.HIGH: [B,C],           GPIO.LOW: [A,D,E,F,G]},
        2: {GPIO.HIGH: [A,B,D,E,G],     GPIO.LOW: [C,F]},
        3: {GPIO.HIGH: [A,B,C,D,G],     GPIO.LOW: [E,F]},
        4: {GPIO.HIGH: [B,C,F,G],       GPIO.LOW: [A,D,E]},
        5: {GPIO.HIGH: [A,C,D,F,G],     GPIO.LOW: [B,E]},
        6: {GPIO.HIGH: [A,C,D,E,F,G],   GPIO.LOW: [B]},
        7: {GPIO.HIGH: [A,B,C],         GPIO.LOW: [D,E,F,G]},
        8: {GPIO.HIGH: [A,B,C,D,E,F,G], GPIO.LOW: []},
        9: {GPIO.HIGH: [A,B,C,F,G],     GPIO.LOW: [D,E]}
        }

'''
Setting the pin to LOW enables the LEDs at position x to be set
'''
position = {
        1: {GPIO.LOW: [D1], GPIO.HIGH: [D2,D3,D4]},
        2: {GPIO.LOW: [D2], GPIO.HIGH: [D1,D3,D4]},
        3: {GPIO.LOW: [D3], GPIO.HIGH: [D1,D2,D4]},
        4: {GPIO.LOW: [D4], GPIO.HIGH: [D1,D2,D3]}
        }

def init_leds():
    '''
    Initialize all required pins to output and put into board mode
    which follows the generic RPi pinout numbering system vice the 
    GPIO number system called BCM. Better for portability.
    '''
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(led_all,GPIO.OUT)

def cleanup_leds():
    '''
    Clears the GPIO pins and performs necessary cleanup.
    '''
    GPIO.cleanup()

def display_decimal():
    '''
    Enable the decimal point pin.
    '''
    GPIO.output(decimal,GPIO.HIGH)

def display_number(num):
    '''
    Sets all of the required high and low pins to correspond with the
    requested number to be displayed. Leverages the led_number dict.
    '''

    hi,lo = led_number[num].keys()
    GPIO.output(led_number[num][hi], hi)
    GPIO.output(led_number[num][lo], lo)


def display_position(pos,num,delay):
    '''
    Sets the required pin to ensure the current position is display
    and then calls the display_number to display the requested num
    in that position. Enables the decimal when on position two to
    simulate the clock colon.
    '''

    if pos == 2:
        display_decimal()
    lo,hi = position[pos].keys()
    GPIO.output(position[pos][lo], lo)
    GPIO.output(position[pos][hi], hi)
    display_number(num)
    time.sleep(delay)
    GPIO.output(led_all, GPIO.LOW)

def get_num_index(number, n):
    '''
    Returns the single digit of index n starting at 0 from the right.
    Example. number=123 n=2 return 1
    '''
    return number // 10**n % 10

def countdown(minutes,seconds):
    '''
    Displays a countdown starting at the provided minute.
    '''

    #bleed off seconds prior to running through minutes
    for sec in reversed(range(seconds)):
        pos1 = get_num_index(minutes,1)
        pos2 = get_num_index(minutes,0)
        pos3 = get_num_index(sec,1)
        pos4 = get_num_index(sec,0)

        for _ in range(200):
            display_position(1, pos1, .00125)
            display_position(2, pos2, .00125)
            display_position(3, pos3, .00125)
            display_position(4, pos4, .00125)

    for m in reversed(range(minutes)):
        pos1 = get_num_index(m,1)
        pos2 = get_num_index(m,0)

        for s in reversed(range(60)):
            pos3 = get_num_index(s,1)
            pos4 = get_num_index(s,0)

            for _ in range(200):
                display_position(1, pos1, .00125)
                display_position(2, pos2, .00125)
                display_position(3, pos3, .00125)
                display_position(4, pos4, .00125)
