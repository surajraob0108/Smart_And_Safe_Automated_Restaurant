#!/usr/bin/env python
import csv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
def RFID_Reader():
    id,text = reader.read()
    print(id)
    with open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/Hospital_DataBase.csv","r") as log:
        patient_details_read = csv.reader(log, delimiter=",")
        result = 0
        for row in patient_details_read:
            if str(row[0]) == str(id) :
                result = 1
                break;
            else:
                result = 0
        print(result)

try:
    RFID_Reader()


    

finally:
        GPIO.cleanup()
