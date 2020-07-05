#!/usr/bin/python

import ssl
import time
import json
import paho.mqtt.client as mqtt
import base64
import threading

# Function for Image Reconstruction
def image_reconstruction(image_data_str):
    image_data = image_data_str.encode('utf-8')                                                               # String to byte conversion                                                       
    image_64_decode = base64.decodebytes(image_data)                                                            
    image_result = open("/home/surajraob0108/Suraj/Python_Programs/Project_Smart_City_IOT/result.jpg", "wb") 
    image_result.write(image_64_decode)
    print("Mask Not Detected")
   # time.sleep(5)
    mask_detection_output = 0
    payload_face_image_data = {"Face_Image_Status":"Mask" , "LED_Status":mask_detection_output}
    publisher_data(topic_customer_details_face_image,payload_face_image_data)
    
# Function for Receiving Customer ID Check status from DataBase
def customer_id_check(database_input):
    if(int(database_input) == 1):
        print("Health Issues")
        id_check = 0
    else:
        print("No Health Issues")
        id_check = 1
    time.sleep(2)
    payload_id_check_data = {"RFID_Status":"RFID" , "LED_Status":id_check}
    publisher_data(topic_customer_details_rfid,payload_id_check_data)

# Function for Customer Temperature Check
def body_temperature_check(body_temperature):
    if(int(body_temperature) <= int(maximum_body_temperature)):
        print("Temperature ok")
        body_temperature_output = 1
    else:
        print("Temperature Not ok")
        body_temperature_output = 0
    payload_temperature_data = {"Temperature_Status":"Temperature" , "LED_Status":body_temperature_output}
    publisher_data(topic_customer_details_temperature,payload_temperature_data)


# Function for Hand Movement Check of Customer
def customer_handdetection_check(input_distance):
    if(int(input_distance) <= int(maximum_handdetection_distance)):
        print("Hand detected: Sanitizer ON")
        buzzer_status = 1
    else:
        print("Hand not detected: Sanitizer OFF")
        buzzer_status = 0
    payload_buzzer_data = {"Buzzer_Status":buzzer_status}
    publisher_data(topic_customer_handdetection,payload_buzzer_data)
    
def customer_presence_table_check(input_table_number,input_customer):
    if(int(input_customer) <= int(maximum_distance)):
        print("Table " +str(input_table_number) + " Not Free..!!")
        led_state = 0
    else:
        print("Table " +str(input_table_number) + " Free..!!")
        led_state = 1
    payload_led_state = {"Table_Number_Output":input_table_number,"Disinfectant_Status":led_state}
    publisher_data(topic_customer_detection,payload_led_state)

def subscriber_start(input_topic):
    while True:
        receiver.subscribe(input_topic,0)
        time.sleep(0.1)

# Function to call publisher to send data 
def publisher_data(input_topic_name,payload_data):
    publish_data = json.dumps(payload_data,indent = 4)
    receiver.publish(input_topic_name,publish_data,0)
    time.sleep(0.1)



def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):
    payload_data = json.loads(msg.payload)
    if(msg.topic == topic_customer_details_face_image):
        image_reconstruction(payload_data["Face_Image"])               
    elif(msg.topic == topic_customer_detection):
        customer_presence_table_check(payload_data["Table_Number"],payload_data["Distance"])
    elif(msg.topic == topic_customer_handdetection):
        customer_handdetection_check(payload_data["Distance"])
    elif(msg.topic == topic_customer_details_temperature):
        body_temperature_check(payload_data["Body_Temperature"])
    elif(msg.topic == topic_hospital_database):
        customer_id_check(payload_data["DataBase_result"])
    else:
        print("Not a valid topic")
        
# AWS IOT certificates       
userdata= "Sensor_Data_Receiver"
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

# Desired User Inputs
maximum_body_temperature = input("Enter body temperature to be checked:")
maximum_handdetection_distance = input("Enter distance to be detected for hand movement:")
maximum_distance = input("Enter distance to be detected for human presence:") 

# MQTT Topic names
topic_customer_details_rfid = "Restaurant/*/Customer_Data/Entry_Details/rfid"
topic_customer_details_temperature = "Restaurant/*/Customer_Data/Entry_Details/temperature"
topic_customer_details_face_image = "Restaurant/*/Customer_Data/Entry_Details/face_image"
topic_customer_detection = "Restaurant/*/Customer_Detection"
topic_customer_handdetection = "Restaurant/*/Customer_HandDetection"
topic_hospital_database = "Restaurant/Database/topic"


threads = []
t0 = threading.Thread(target=subscriber_start,args=[topic_hospital_database]) 
threads.append(t0)
t0.start() 
t1 = threading.Thread(target=subscriber_start,args=[topic_customer_details_temperature]) 
threads.append(t1)
t1.start()
t2 = threading.Thread(target=subscriber_start,args=[topic_customer_details_face_image]) 
threads.append(t2)
t2.start()
t3 = threading.Thread(target=subscriber_start,args=[topic_customer_detection]) 
threads.append(t3)
t3.start()
t4 = threading.Thread(target=subscriber_start,args=[topic_customer_handdetection]) 
threads.append(t4)
t4.start()

for j in threads:
    j.join


""" while True:
    receiver.subscribe(topic_hospital_database,0)
    time.sleep(0.1)
    receiver.subscribe(topic_customer_details_rfid,0)
    time.sleep(0.1)
    receiver.subscribe(topic_customer_detection,0)
    time.sleep(0.1)
    receiver.subscribe(topic_customer_handdetection,0)
    time.sleep(0.1) """

    
    
    
    
