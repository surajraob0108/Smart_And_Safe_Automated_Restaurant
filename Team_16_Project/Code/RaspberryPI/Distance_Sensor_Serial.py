#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading

def distance_calculation_1(Trigger_IN_1,ECHO_OUT_1):    
    GPIO.output(Trigger_IN_1, GPIO.LOW)
    time.sleep(1)
    GPIO.output(Trigger_IN_1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger_IN_1, GPIO.LOW)
    while GPIO.input(ECHO_OUT_1)==0:
        pulse_start_time_1 = time.time()
    while GPIO.input(ECHO_OUT_1)==1:
        pulse_end_time_1 = time.time()
    pulse_duration_1 = pulse_end_time_1 - pulse_start_time_1
    distance_1 = round(pulse_duration_1 * 17150, 2)
    print "Data ",str(Trigger_IN_1),"-",str(ECHO_OUT_1)," Distance:",distance_1,"cm"
    
def distance_calculation_2(Trigger_IN_2,ECHO_OUT_2):    
    GPIO.output(Trigger_IN_2, GPIO.LOW)
    time.sleep(1.5)
    GPIO.output(Trigger_IN_2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger_IN_2, GPIO.LOW)
    while GPIO.input(ECHO_OUT_2)==0:
        pulse_start_time_2 = time.time()
    while GPIO.input(ECHO_OUT_2)==1:
        pulse_end_time_2 = time.time()
    pulse_duration_2 = pulse_end_time_2 - pulse_start_time_2
    distance_2 = round(pulse_duration_2 * 17150, 2)
    print "Data ",str(Trigger_IN_2),"-",str(ECHO_OUT_2)," Distance:",distance_2,"cm"
    
def distance_calculation_3(Trigger_IN_3,ECHO_OUT_3):    
    GPIO.output(Trigger_IN_3, GPIO.LOW)
    time.sleep(2)
    GPIO.output(Trigger_IN_3, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger_IN_3, GPIO.LOW)
    while GPIO.input(ECHO_OUT_3)==0:
        pulse_start_time_3 = time.time()
    while GPIO.input(ECHO_OUT_3)==1:
        pulse_end_time_3 = time.time()
    pulse_duration_3 = pulse_end_time_3 - pulse_start_time_3
    distance_3 = round(pulse_duration_3 * 17150, 2)
    print "Data ",str(Trigger_IN_3),"-",str(ECHO_OUT_3)," Distance:",distance_3,"cm"

def distance_calculation_4(Trigger_IN_4,ECHO_OUT_4):    
    GPIO.output(Trigger_IN_4, GPIO.LOW)
    time.sleep(2.5)
    GPIO.output(Trigger_IN_4, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trigger_IN_4, GPIO.LOW)
    while GPIO.input(ECHO_OUT_4)==0:
        pulse_start_time_4 = time.time()
    while GPIO.input(ECHO_OUT_4)==1:
        pulse_end_time_4 = time.time()
    pulse_duration_4 = pulse_end_time_4 - pulse_start_time_4
    distance_4 = round(pulse_duration_4 * 17150, 2)
    print "Data ",str(Trigger_IN_4),"-",str(ECHO_OUT_4)," Distance:",distance_4,"cm"
    
# def distance_calculation_5(Trigger_IN_5,ECHO_OUT_5):    
#     GPIO.output(Trigger_IN_5, GPIO.LOW)
#     time.sleep(3)
#     GPIO.output(Trigger_IN_5, GPIO.HIGH)
#     time.sleep(0.00001)
#     GPIO.output(Trigger_IN_5, GPIO.LOW)
#     while GPIO.input(ECHO_OUT_5)==0:
#         pulse_start_time_5 = time.time()
#     while GPIO.input(ECHO_OUT_5)==1:
#         pulse_end_time_5 = time.time()
#     pulse_duration_5 = pulse_end_time_5 - pulse_start_time_5
#     distance_5 = round(pulse_duration_5 * 17150, 2)
#     print "Data ",str(Trigger_IN_5),"-",str(ECHO_OUT_5)," Distance:",distance_5,"cm"

try:
      GPIO.setmode(GPIO.BOARD)
      PIN_TRIGGER_IN = [3 ,7, 8 , 13 ]
      PIN_ECHO_OUT = [5 ,11, 10 , 15 ]         
      GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
      GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
      threads = []
      start = time.time()
      for a in range(0,2):
          t1 = threading.Thread(target=distance_calculation_1,args=(PIN_TRIGGER_IN[0],PIN_ECHO_OUT[0]))
          threads.append(t1)
          t1.start()
          t2 = threading.Thread(target=distance_calculation_2,args=(PIN_TRIGGER_IN[1],PIN_ECHO_OUT[1]))
          threads.append(t2)
          t2.start()
          t3= threading.Thread(target=distance_calculation_3,args=(PIN_TRIGGER_IN[2],PIN_ECHO_OUT[2]))
          threads.append(t3)
          t3.start()
          t4 = threading.Thread(target=distance_calculation_4,args=(PIN_TRIGGER_IN[3],PIN_ECHO_OUT[3]))
          threads.append(t4)
          t4.start()
#           t5 = threading.Thread(target=distance_calculation_5,args=(PIN_TRIGGER_IN[4],PIN_ECHO_OUT[4]))
#           threads.append(t5)
#           t5.start()
          for j in threads:
              j.join();
      end = time.time()
      print("Total time : " + str(end-start))
finally:
      GPIO.cleanup()
