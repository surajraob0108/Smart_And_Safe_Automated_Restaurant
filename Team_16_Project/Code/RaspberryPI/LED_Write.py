#!/usr/bin/python
import RPi.GPIO as GPIO
import time
try:
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(7,GPIO.OUT)
      print "LED on"
      GPIO.output(7,GPIO.HIGH)
      time.sleep(1)
      print "LED off"
      GPIO.output(7,GPIO.LOW)
finally:
      GPIO.cleanup()