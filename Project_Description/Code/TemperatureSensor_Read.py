#!/usr/bin/env python

import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.IN)
    while True:
        input_value = GPIO.input(11)
        if input_value == 1:
            print(input_value)
            break;    
finally:
    GPIO.cleanup()
