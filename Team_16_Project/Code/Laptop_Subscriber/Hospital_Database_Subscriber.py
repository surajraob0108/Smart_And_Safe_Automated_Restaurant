#!/usr/bin/python

import ssl
import time
import json
import paho.mqtt.client as mqtt
import csv

# Function for reading database
def database_reader(input_customer_id):
    with open("/home/surajraob0108/Suraj/Python_Programs/Project_Smart_City_IOT/Programs/Subscriber/Hospital_DataBase.csv","r") as log:
        patient_details_read = csv.reader(log, delimiter=",")
        for row in patient_details_read:
            if str(row[0]) == str(input_customer_id):
                result_rfid = 1
                print("User Details Found")
                break
            else:
                result_rfid = 0
           
    payload_result = {"DataBase_result":result_rfid}
    payload_data = json.dumps(payload_result,indent=4)
    receiver.publish(topic_hospital_database,payload_data,0)
    time.sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):
    payload_data = json.loads(msg.payload)
    database_reader(payload_data["Customer_ID"])
    time.sleep(0.1)

# AWS IOT certificates       
userdata= "Hospital_DataBase"
awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"  
awsport = 8883

caPath = "/home/surajraob0108/Suraj/Python_Programs/Project_Smart_City_IOT/Certificates/AmazonRootCA1.pem"
certPath = "/home/surajraob0108/Suraj/Python_Programs/Project_Smart_City_IOT/Certificates/0b5fd75186-certificate.pem.crt"
keyPath = "/home/surajraob0108/Suraj/Python_Programs/Project_Smart_City_IOT/Certificates/0b5fd75186-private.pem.key"

receiver = mqtt.Client(userdata)
receiver.on_connect = on_connect 
receiver.on_message = on_message

receiver.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
receiver.connect(awshost, awsport, keepalive=60)
receiver.loop_start()
time.sleep(0.1)

# MQTT Topic names
topic_customer_details_rfid = "Restaurant/*/Customer_Data/Entry_Details/rfid"
topic_hospital_database = "Restaurant/Database/topic"

while True:
    receiver.subscribe(topic_customer_details_rfid,0)
    time.sleep(0.1)