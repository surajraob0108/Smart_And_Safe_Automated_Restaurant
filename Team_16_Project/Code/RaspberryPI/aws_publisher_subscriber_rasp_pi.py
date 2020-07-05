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
global rfid_start
global temperature_start

# Image Input
def camera_input():
    while True:
    
        
#     os.system("wget 192.168.0.3:8080/photo.jpg")
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
        payload_image_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Face_Image":image_data}
        publisher_data(topic_customer_details_face_image,payload_image_data)
        time.sleep(4)
        
# RFID Input
def rfid_input():
    while True:
   
            #rfid,text = reader.read()
        rfid = 17839425354
        #print(rfid)
        payload_rfid_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Customer_ID":rfid}
        publisher_data(topic_customer_details_rfid,payload_rfid_data)
        time.sleep(5)

# Temperature Input
def temperature_sensor_input(pin):
    while True:
        # Temperature Check
        #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = 22.0
        
        payload_temperature_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Body_Temperature":temperature}
        publisher_data(topic_customer_details_temperature,payload_temperature_data)
        time.sleep(3)    
    
# Distance calculation Input
def distance_calculation(Trigger_IN,ECHO_OUT,sleeptime,table_number):
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
        #print ("Data ",Trigger_IN,"-",ECHO_OUT," Distance:",distance,"cm")
        
        if(table_number <=3):
            payload_table_data = {"Restaurant_number":restaurant_number,"Table_Number":table_number,"Distance":distance}
            publisher_data(topic_customer_detection,payload_table_data)
        else:
            
            payload_hand_detection = {"Restaurant_number":restaurant_number,"Distance":distance}
            publisher_data(topic_customer_handdetection,payload_hand_detection)
        time.sleep(2)

#Active Buzzer Output  - Hand Sanitizer
def hand_sanitiser_status(input_buzzer_state):
    if(int(input_buzzer_state) == 1):
        print("Buzzer ON")
        buzzState = False
        for i in range(0,4):
            buzzState = not buzzState
            GPIO.output(BUZZER_OUT, buzzState)
            time.sleep(0.5)        
    else:
        print("Buzzer OFF")


        
#LED Output - Disinfectant_Status for each table
def disinfectant_status(input_table_number,input_led_state):
    if(int(input_table_number) == 1):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE1_OUT,1)
        else:
            print("Table "+str(input_table_number)+":Disinfectant OFF")
    elif(int(input_table_number) == 2):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE2_OUT,1)
        else:
            print("Table "+str(input_table_number)+":Disinfectant OFF")
    elif(int(input_table_number) == 3):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE3_OUT,1)
        else:
            print("Table "+str(input_table_number)+":Disinfectant OFF")
    else:
        print("Not a valid table value")

#Function for LED ON/OFF
def led_on_off(output_pin,ontime):
    GPIO.output(output_pin,GPIO.HIGH)
    time.sleep(ontime)
    GPIO.output(output_pin,GPIO.LOW)
    
#LED Output - Entry allowed/denied to Restaurant        
def customer_entry(input_customer_check,input_led_status):    
    if(input_customer_check == "Temperature"):
        if(int(input_led_status) == 1):
            print("Customer:" +str(input_customer_check)+ "allowed")
        else:
            led_on_off(LED_TEMPERATURE_OUT,1)            
            
    elif(input_customer_check == "Mask"):
        if(int(input_led_status) == 1):
            # Code to changed after Tensor flow
            led_on_off(LED_MASK_OUT,1)
        else:
            print("Customer:" +str(input_customer_check)+ " Not allowed")
            
    elif(input_customer_check == "RFID"):
        if(int(input_led_status) == 1):
            print("Customer:" +str(input_customer_check)+ " allowed")
        else:
            led_on_off(LED_RFID_OUT,1)
    else:
        print("Customer check yet going on")
        
        
# Function to receive actuator data         
def subscriber_start(input_subscriber_topic_name):
    while True:

        myclient.subscribe(input_subscriber_topic_name,0)
        time.sleep(0.1)
    

def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):
    
    if(msg.topic == topic_customer_details_rfid):
        payload_data = json.loads(msg.payload)
        customer_entry(payload_data["RFID_Status"],payload_data["LED_Status"])
    elif(msg.topic == topic_customer_details_temperature):
        payload_data = json.loads(msg.payload)
        customer_entry(payload_data["Temperature_Status"],payload_data["LED_Status"])
    elif(msg.topic == topic_customer_details_face_image):
        payload_data = json.loads(msg.payload)
        customer_entry(payload_data["Face_Image_Status"],payload_data["LED_Status"])
    elif(msg.topic == topic_customer_detection):
        payload_data = json.loads(msg.payload)
        disinfectant_status(payload_data["Table_Number_Output"],payload_data["Disinfectant_Status"])
    elif(msg.topic == topic_customer_handdetection):
        payload_data = json.loads(msg.payload)
        hand_sanitiser_status(payload_data["Buzzer_Status"])
    else:
        print("No valid topic")

# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,0)
    time.sleep(0.1)
    
# User Inputs   
restaurant_location = input("Enter Restaurant Location:")
restaurant_number = input("Enter Restaurant Number:")

# MQTT Topic Names
topic_customer_details_rfid = "Restaurant/*/Customer_Data/Entry_Details/rfid"
topic_customer_details_temperature = "Restaurant/*/Customer_Data/Entry_Details/temperature"
topic_customer_details_face_image = "Restaurant/*/Customer_Data/Entry_Details/face_image"
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
    BUZZER_OUT = 40
    LED_TEMPERATURE_OUT = 38
    LED_MASK_OUT = 37
    LED_RFID_OUT = 35
    LED_TABLE1_OUT = 18
    LED_TABLE2_OUT = 32
    LED_TABLE3_OUT = 33
    TEMPERATURE_PIN = 7
    GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
    GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
    GPIO.setup(BUZZER_OUT, GPIO.OUT)
    GPIO.setup(LED_TEMPERATURE_OUT, GPIO.OUT)
    GPIO.setup(LED_MASK_OUT, GPIO.OUT)
    GPIO.setup(LED_RFID_OUT, GPIO.OUT)
    GPIO.setup(LED_TABLE1_OUT, GPIO.OUT)
    GPIO.setup(LED_TABLE2_OUT, GPIO.OUT)
    GPIO.setup(LED_TABLE3_OUT, GPIO.OUT)
    
    threads = []

    t0 = threading.Thread(target=rfid_input,args=[],daemon=True)
    threads.append(t0)
    t0.start()
    t1 = threading.Thread(target=camera_input,args=[],daemon=True)
    threads.append(t1)
    t1.start()
    t2 = threading.Thread(target=temperature_sensor_input,args=[TEMPERATURE_PIN],daemon=True)
    threads.append(t2)
    t2.start()
           
          # 4 sensors currently interfaced
    for i in range(1,4):
        t3 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[i],PIN_ECHO_OUT[i],i*0.5,i),daemon=True)
        threads.append(t3)
        t3.start()
    t4 = threading.Thread(target=distance_calculation,args=(PIN_TRIGGER_IN[0],PIN_ECHO_OUT[0],0.1,4),daemon=True)
    threads.append(t4)
    t4.start()
    t5 = threading.Thread(target=subscriber_start,args=[topic_customer_detection],daemon=True)
    threads.append(t5)
    t5.start()
    t6 = threading.Thread(target=subscriber_start,args=[topic_customer_details_rfid],daemon=True)
    threads.append(t6)
    t6.start()
    t7 = threading.Thread(target=subscriber_start,args=[topic_customer_details_temperature],daemon=True)
    threads.append(t7)
    t7.start()
    t8 = threading.Thread(target=subscriber_start,args=[topic_customer_details_face_image],daemon=True)
    threads.append(t8)
    t8.start()
    t9 = threading.Thread(target=subscriber_start,args=[topic_customer_handdetection],daemon=True)
    threads.append(t9)
    t9.start()

    for j in threads:
        j.join();
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Close")

    



