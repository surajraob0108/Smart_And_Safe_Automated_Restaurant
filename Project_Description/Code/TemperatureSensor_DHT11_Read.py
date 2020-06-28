#!/usr/bin/python
import RPi.GPIO as GPIO
import Python_DHT
import time

sensor = Python_DHT.DHT11


    
try:
    pin = 4 # PIN 26
    GPIO.setmode(GPIO.BOARD)
    for a in range(0,4):
        humidity, temperature = Python_DHT.read_retry(sensor, pin)     
        print("Temperature = "+str(temperature))
        time.sleep(1)

finally:
       GPIO.cleanup()