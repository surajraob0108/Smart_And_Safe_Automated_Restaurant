import RPi.GPIO as GPIO
import time

try:
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(7,GPIO.OUT)
      buzzState = False
      for i in range(0,20):
        buzzState = not buzzState
        GPIO.output(7, buzzState)
        time.sleep(1)
finally:
      GPIO.cleanup()