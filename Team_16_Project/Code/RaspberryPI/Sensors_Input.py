#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
from mfrc522 import SimpleMFRC522
import csv
import Python_DHT

reader = SimpleMFRC522()    
sensor = Python_DHT.DHT11

# Input Check - RFID, Temperature , Mask
def input_check(pin):
    # RFID Check
    while True:
        id,text = reader.read()
        print(id)
        with open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/Hospital_DataBase.csv","r") as log:
            patient_details_read = csv.reader(log, delimiter=",")
            result_rfid = 0 
            for row in patient_details_read:
                if str(row[0]) == str(id) :
                    result_rfid = 1
                    break;
                else:
                    result_rfid = 0
            print("Result_RFID: " + str(result_rfid))
        time.sleep(1)
        
        # Temperature Check
        humidity, temperature = Python_DHT.read_retry(sensor, pin)     
        print("Temperature = "+str(temperature))
        result_temp = 0
        if temperature <=30:
            result_temp = 1
        else:
            result_temp = 0
        print("Result_Temperature: " + str(result_temp))
        #
        time.sleep(3)
        #return result_rfid,result_temp
# Distance calculation Input
def distance_calculation(Trigger_IN,ECHO_OUT,sleeptime):
    while True:
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
        print ("Data ",Trigger_IN,"-",ECHO_OUT," Distance:",distance,"cm")
        result_distance = 0
        if Trigger_IN == 3:
            if distance <= 15:
                result_distance = 1
            else:
                result_distance = 0
        else:
            if distance <= 75:
                result_distance = 1
            else:
                result_distance = 0
        print("Distance Result: "  + str(result_distance));   
        time.sleep(2)
#Active Buzzer Output - Entry to Restaurant
#LED Output - Hand Sanitizer    
try:

      
      GPIO.setmode(GPIO.BOARD)
      PIN_TRIGGER_IN = [3 ,7, 8 , 13 ] # PI - Sensor
      PIN_ECHO_OUT = [5 ,11, 10 , 15 ] # Sensor - PI
      TEMPERATURE_PIN = 7
      GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
      GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
      threads = []
       
      t0 = threading.Thread(target=input_check,args=[TEMPERATURE_PIN])
      threads.append(t0)
      t0.start()
          
          # 4 sensors currently interfaced
      for i in range(1,4):
          
          t1 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[i],PIN_ECHO_OUT[i],i*0.5))
          threads.append(t1)
          t1.start()
      t2 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[0],PIN_ECHO_OUT[0],2))
      threads.append(t2)
      t2.start()
          
      for j in threads:
          
          j.join();
        

finally:
      GPIO.cleanup()

