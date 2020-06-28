#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
my_lock = threading.Lock()

class Mythread(threading.Thread):
    def __init__(self,sensor_num,pin_trigger,pin_echo,sleeptime):
        threading.Thread.__init__(self)
        self.sensor_num = sensor_num
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.sleeptime = sleeptime
    def run(self):
        print("Sensor_num : " + str(self.sensor_num) + "\n")
        distance_calculation(self.pin_trigger,self.pin_echo,self.sleeptime) 
    
# Distance calculation function

def distance_calculation(Trigger_IN,ECHO_OUT,sleeptime):
    my_lock.acquire()
    GPIO.output(Trigger_IN, GPIO.LOW)
    time.sleep(sleeptime)
    GPIO.output(Trigger_IN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger_IN, GPIO.LOW)
    
    while GPIO.input(ECHO_OUT)==0:
        pulse_start_time = time.time()
    while GPIO.input(ECHO_OUT)==1:
        pulse_end_time = time.time()
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    
    print "Data ",str(Trigger_IN),"-",str(ECHO_OUT)," Distance:",distance,"cm"
    my_lock.release()
    
try:
      GPIO.setmode(GPIO.BOARD)
      PIN_TRIGGER_IN = [3 ,7, 8 , 13 ] # PI - Sensor
      PIN_ECHO_OUT = [5 ,11, 10 , 15 ] # Sensor - PI       
      GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
      GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
      threads = []
      # to calculate sensor values twice
      for a in range(0,2):
          # 3 sensors currently interfaced
          for i in range(1,5):
              t = Mythread(i,PIN_TRIGGER_IN[i-1],PIN_ECHO_OUT[i-1],2)
              threads.append(t)
              t.start()
          for j in threads:
              j.join();

finally:
      GPIO.cleanup()
