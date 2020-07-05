#!/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
reader = SimpleMFRC522()

try:
    
    id,text = reader.read()
    time.sleep(2)
    print(id)

finally:
        GPIO.cleanup()
