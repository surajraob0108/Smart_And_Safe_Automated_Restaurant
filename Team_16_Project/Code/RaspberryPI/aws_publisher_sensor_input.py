#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
from mfrc522 import SimpleMFRC522
import Adafruit_DHT
import ssl
import paho.mqtt.client as mqtt
import json
from PIL import Image
from resizeimage import resizeimage
import base64
import os
global restaurant_number

# Image Input
def camera_input():
    #os.system("wget 192.168.0.3:8080/photo.jpg")
#     time.sleep(2)
#     with open("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo.jpg", "r+b") as f:
#         with Image.open(f) as image:
#             cover = resizeimage.resize_cover(image, [200, 100])
#             cover.save("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg", image.format)
        
    image_updated = open("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg", "rb")
    image_read = image_updated.read()
    image_64_encode = base64.encodebytes(image_read)
    image_data = image_64_encode.decode("utf-8")
    #os.remove("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg")
    #.remove("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs//photo.jpg")    
    return image_data

# RFID Input
def rfid_input():
    #id,text = reader.read()
    id = 717839425354
    #print(id)
    return id

# Temperature Input
def temperature_sensor_input(pin):
    # Temperature Check
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature_value = 28.0
    return temperature_value

# Customer Entry Details Input
def customer_entry_details(temperature_pin):
    #while True:
    rfid = rfid_input()
    time.sleep(1)
    image = camera_input()
    time.sleep(1)
    temperature = temperature_sensor_input(temperature_pin)    
    payload_customer_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Customer_ID":rfid ,"Face_Image":image,"Body_Temperature":temperature}
    customer_data= json.dumps(payload_customer_data,indent=4)
    myclient.publish(topic_customer_details,customer_data,0)
    time.sleep(0.1)
    
# Distance calculation Input
def distance_calculation(Trigger_IN,ECHO_OUT,sleeptime,table_number):
    #while True:
        
#         GPIO.output(Trigger_IN, GPIO.LOW)
#         time.sleep(sleeptime)
#         GPIO.output(Trigger_IN, GPIO.HIGH)
#         time.sleep(0.00001)
#         GPIO.output(Trigger_IN, GPIO.LOW)
#         while GPIO.input(ECHO_OUT)==0:
#             pulse_start_time = time.time()
#         while GPIO.input(ECHO_OUT)==1:
#             pulse_end_time = time.time()
#         pulse_duration = pulse_end_time - pulse_start_time
#         distance = round(pulse_duration * 17150, 2)
#         print ("Data ",Trigger_IN,"-",ECHO_OUT," Distance:",distance,"cm")
        distance = table_number + 10
        if(table_number <=3):
            payload_table_data = {"Restaurant_number":restaurant_number,"Table_Number":table_number,"Distance":distance}
            table_data = json.dumps(payload_table_data,indent=4)        
            myclient.publish(topic_customer_detection,table_data,0)
        else:
            payload_hand_detection = {"Restaurant_number":restaurant_number,"Distance":distance}
            hand_detection_data = json.dumps(payload_hand_detection,indent=4)
            myclient.publish(topic_customer_handdetection,hand_detection_data,0)
        time.sleep(2)

#LED Output - Hand Sanitizer
def hand_sanitiser_status(input_led_blink):
    if(int(input_led_blink) == 1):
        print("LED ON")
    else:
        print("LED OFF")
        
#LED Output - Disinfectant_Status for each table
def disinfectant_status(input_table_number,input_led_state):
    
    if(int(input_led_state) == 1):
        print("Table "+str(input_table_number)+":Disinfectant ON")
    else:
        print("Table "+str(input_table_number)+":Disinfectant OFF")
        
#Active Buzzer Output - Entry allowed/denied to Restaurant        
def customer_entry(input_buzzer_state):
    if(int(input_buzzer_state) == 1):
        print("Customer allowed")
    else:
        print("Customer Not allowed")
        
# Function to receive actuator data         
def subscribers_running():
    while True:
        myclient.subscribe(topic_customer_details,0)
        time.sleep(0.1)
        myclient.subscribe(topic_customer_detection,0)
        time.sleep(0.1)
        myclient.subscribe(topic_customer_handdetection,0)        
        time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):
    payload_data = json.loads(msg.payload)
    if(msg.topic == topic_customer_details):
        customer_entry(payload_data["Buzzer_Status"])
    elif(msg.topic == topic_customer_detection):
        disinfectant_status(payload_data["Table_Number_Output"],payload_data["Disinfectant_Status"])
    elif(msg.topic == topic_customer_handdetection):
        hand_sanitiser_status(payload_data["LED_Status"])
    else:
        print("No valid topic")
     
        
    

    
restaurant_location = input("Enter Restaurant Location:")
restaurant_number = input("Enter Restaurant Number:")
topic_customer_details = "Restaurant/*/Customer_Data/Entry_Details"
topic_customer_detection = "Restaurant/*/Customer_Detection"
topic_customer_handdetection = "Restaurant/*/Customer_HandDetection"
#reader = SimpleMFRC522()
GPIO.setwarnings(False)
sensor=Adafruit_DHT.DHT11

# Certificates for AWS IOT Services
awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"   
awsport = 8883
caPath = "/home/pi/Public/Team_16_Project/Certificates/AmazonRootCA1.pem"
certPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-private.pem.key"
 
myclient = mqtt.Client("Sensor_Data_Publisher")
myclient.on_connect = on_connect 
myclient.on_message = on_message
myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)

myclient.loop_start()
# Delay needed for connection
time.sleep(0.1)
try:
        
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER_IN = [3 ,7, 8 , 13 ] # PI - Sensor
    PIN_ECHO_OUT = [5 ,11, 10 , 15 ] # Sensor - PI
    TEMPERATURE_PIN = 7
    GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
    GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
    threads = []

    t0 = threading.Thread(target=customer_entry_details,args=[TEMPERATURE_PIN],daemon=True)
    threads.append(t0)
    t0.start()
           
          # 4 sensors currently interfaced
    for i in range(1,4):
        t1 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[i],PIN_ECHO_OUT[i],i*0.5,i),daemon=True)
        threads.append(t1)
        t1.start()
    t2 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[0],PIN_ECHO_OUT[0],2,4),daemon=True)
    threads.append(t2)
    t2.start()
    t3 = threading.Thread(target=subscribers_running,args=[],daemon=True)
    threads.append(t3)
    t3.start()
    for j in threads:
        j.join();
        
except KeyboardInterrupt:
    print("Close")

    


