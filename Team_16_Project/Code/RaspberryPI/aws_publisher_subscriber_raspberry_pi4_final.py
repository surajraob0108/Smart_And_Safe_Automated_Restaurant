#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
import Adafruit_DHT
import ssl
import paho.mqtt.client as mqtt
import json
from PIL import Image
from resizeimage import resizeimage
import base64
import os
import sys
from firebase import firebase
from datetime import date

sensor_health_status = ["Good","Good","Good","Good","Good","Good","Good"]
# Camera Input
def camera_input():
    return_value = os.system("wget 192.168.0.2:8080/photo.jpg >/dev/null 2>&1")
    time.sleep(1)
    if(return_value == 1024):
        sensor_health_status[1] = "Bad"
        f = open("/home/pi/Public/Team_16_Project/Sensor_Programs/photo.jpg", "r+b")
    else:
        sensor_health_status[1] = "Good"
        f = open("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo.jpg", "r+b")
    image = Image.open(f)
    cover = resizeimage.resize_cover(image, [200, 100])
    cover.save("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg", image.format)   

    image_updated = open("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg", "rb")
    image_read = image_updated.read()
    image_64_encode = base64.encodebytes(image_read)
    image_data = image_64_encode.decode("utf-8")
    if(return_value != 1024):
        os.remove("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo.jpg")
    os.remove("/home/pi/Public/Team_16_Project/Sensor_Programs/Programs/photo_resize.jpg")
    print("Image Captured")
    return image_data

# Customer_ID Generation based on distance 
def customer_id_generation(input_distance):
    input_distance_value = int(input_distance)
    sensor_health_status[0] = "Good"
    if(input_distance_value == 0):
        customer_id = 2345678900
        sensor_health_status[0] = "Bad"
    elif(input_distance_value >=1 and input_distance_value <= 4):
        customer_id = 1234567888
    elif(input_distance_value >= 5 and input_distance_value <= 8):
        customer_id = 1112223334
    elif(input_distance_value >= 9 and input_distance_value <= 12):
        customer_id = 1234567890
    elif(input_distance_value >= 13 and input_distance_value <= 16):
        customer_id = 2345678908
    elif(input_distance_value >= 17 and input_distance_value <= 20):
        customer_id = 3456789003
    elif(input_distance_value >= 21 and input_distance_value <= 24):
        customer_id = 2345678905
    elif(input_distance_value >= 25 and input_distance_value <= 28):
        customer_id = 4567890001
    elif(input_distance_value >= 29 and input_distance_value <= 32):
        customer_id = 3456789006
    elif(input_distance_value >= 33 and input_distance_value <= 36):
        customer_id = 2345678905
    elif(input_distance_value >= 37 and input_distance_value <= 40):
        customer_id = 4567890008
    else:
        print("customer Id still generating")
        
    return customer_id

# Temperature Input
def temperature_sensor_input(pin):    
    sensor_health_status[2] = "Good"
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin,2,1)
    # Default value in case if the temperature sensor not working
    if(str(temperature) == "None"):
        temperature= 50
        sensor_health_status[2] = "Bad"
        
    print("Temperature:"+str(temperature))
    return temperature  
    
# Distance calculation Input
def distance_calculation(Trigger_IN,ECHO_OUT,sleeptime):   
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
    return distance

# Function for Customer Hand Movement Detection
def customer_movement_hand_detection(PIN_IN,PIN_OUT,sleep_time):
    sensor_health_status[6] = "Good"
    while True:
        hand_distance = distance_calculation(PIN_IN,PIN_OUT,sleep_time)
        if(int(hand_distance) == 0):
            sensor_health_status[6] = "Bad"
        payload_handdetection = {"Restaurant_number":restaurant_number,"Distance":hand_distance}
        publisher_data(topic_customer_handdetection,payload_handdetection)
        time.sleep(2)

# Customer Detection Table Check
def customer_presence_table_data(PIN_IN_1,PIN_OUT_1,sleep_time_1,PIN_IN_2,PIN_OUT_2,sleep_time_2,PIN_IN_3,PIN_OUT_3,sleep_time_3):
    sensor_health_status[3] = "Good"
    sensor_health_status[4] = "Good"
    sensor_health_status[5] = "Good"
    while True:
        table_1_distance = distance_calculation(PIN_IN_1,PIN_OUT_1,sleep_time_1)
        table_2_distance = distance_calculation(PIN_IN_2,PIN_OUT_2,sleep_time_2)
        table_3_distance = distance_calculation(PIN_IN_3,PIN_OUT_3,sleep_time_3)
        if(int(table_1_distance) == 0):
            sensor_health_status[3] = "Bad"            
        if(int(table_2_distance) == 0):
            sensor_health_status[4] = "Bad"
        if(int(table_3_distance) == 0):
            sensor_health_status[5] = "Bad"        
        payload_table_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Distance_Table1":table_1_distance,"Distance_Table2":table_2_distance,"Distance_Table3":table_3_distance}
        publisher_data(topic_customer_detection,payload_table_data)
        time.sleep(10)
        
def customer_entry_details(input_trig_pin,input_echo_pin,sleeptime,temperature_pin):
    while True:
        distance_id = distance_calculation(input_trig_pin,input_echo_pin,sleeptime)
        if(distance_id <=40):
            customer_unique_id = customer_id_generation(distance_id)
            print("CustomerID:"+str(customer_unique_id))
            time.sleep(2)
            face_image_data = camera_input()
            time.sleep(1)
            temperature_data = temperature_sensor_input(temperature_pin)
            payload_customer_data = {"Location":restaurant_location,"Restaurant_number":restaurant_number,"Customer_ID":customer_unique_id,"Face_Image":face_image_data,"Body_Temperature":temperature_data}
            publisher_data(topic_customer_details,payload_customer_data)
        else:
            waiting_for_customer = 1

def customer_entry_result(input_customer_entry_data):
    if(int(input_customer_entry_data) == 1):
        print("Customer Allowed")
        led_on_off(ENTRY_ACCEPTED,2)
    else:
        print("Customer Denied")
        led_on_off(ENTRY_DENIED,2)
        
#Function for LED ON/OFF
def led_on_off(output_pin,ontime):
    GPIO.output(output_pin,GPIO.HIGH)
    time.sleep(ontime)
    GPIO.output(output_pin,GPIO.LOW)

#Active Buzzer Output  - Hand Sanitizer
def hand_sanitiser_status(input_buzzer_state):
    if(int(input_buzzer_state) == 1):
        print("BuzzerOn")
        buzzState = False
        for i in range(0,4):
            buzzState = not buzzState
            GPIO.output(BUZZER_OUT, buzzState)
            time.sleep(0.5)        

#LED Output - Disinfectant_Status for each table
def disinfectant_status(input_table_number,input_led_state):
    if(int(input_table_number) == 1):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE1_OUT,1)
    elif(int(input_table_number) == 2):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE2_OUT,1)
    elif(int(input_table_number) == 3):
        if(int(input_led_state) == 1):
            led_on_off(LED_TABLE3_OUT,1)
    else:
        print("Not a valid table value")

# Writing Sensor Health Status to Database
def writeToFirebase():
    while True:
        if "Bad" in sensor_health_status:
            print("DataBase entered")
            firebase1 = firebase.FirebaseApplication('https://sssr-sensorhealth.firebaseio.com/', None)

            data1 = {'Restaurant_ID': restaurant_number,
                     'ID_Ultrasonic_Distance_Sensor': sensor_health_status[0],
                     'Camera': sensor_health_status[1],
                     'Temperature_Sensor': sensor_health_status[2],                     
                     'Table1_Ultrasonic_Distance_Sensor': sensor_health_status[3],
                     'Table2_Ultrasonic_Distance_Sensor': sensor_health_status[4],
                     'Table3_Ultrasonic_Distance_Sensor': sensor_health_status[5],
                     'Hand_Detection_Ultrasonic_Distance_Sensor': sensor_health_status[6]
                     }
            firebase1.post("location/" + restaurant_location + "/" + date.today().strftime('%d-%m-%Y'), data1)
            print("Sensor Health issue.Run Diagnostics..!!")
        time.sleep(30)
# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,0)
    time.sleep(0.1)

# Function to receive actuation data         
def subscriber_start(input_subscriber_topic_name):
    while True:
        myclient.subscribe(input_subscriber_topic_name,0)
        time.sleep(0.1)
        
# Confirmation on connection 
def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

# Confirmation on message callback    
def on_message(client, userdata, msg):
    if(msg.topic == topic_customer_details):
        payloadblockPrint_customer_result = json.loads(msg.payload)
        customer_entry_result(payload_customer_result["Customer_Entry_Result"])
    elif(msg.topic == topic_customer_detection):
        payload_data = json.loads(msg.payload)
        disinfectant_status(payload_data["Table_Number_Output"],payload_data["Disinfectant_Status"])
    elif(msg.topic == topic_customer_handdetection):
        payload_data = json.loads(msg.payload)
        hand_sanitiser_status(payload_data["Buzzer_Status"])
    else:
        print("No valid topic")
    
# Validate User Input - Restaurant Location
def valid_restaurant_location():
    while True:
        global restaurant_location
        restaurant_location = input("Enter Restaurant Location:")
        if(restaurant_location == "Stuttgart" or restaurant_location == "Boblingen" or restaurant_location == "Esslingen" or restaurant_location == "Ludwigsburg"):
            print("Entered Restaurant location is correct")
            break;
        else:
            print("Please enter a valid restaurant location")

# Validate User Input - Restaurant Number
def valid_restaurant_number():
    while True:
        global restaurant_number 
        restaurant_number = input("Enter Restaurant Number:")
        int_restaurant_number = int(restaurant_number)
        if(int_restaurant_number == 0 or int_restaurant_number ==1 or int_restaurant_number ==2 or int_restaurant_number ==3):
            print("Entered Restaurant number is correct")
            print("Customer Scanning Started..!!")
            print("Hand Santizer:Processing Hand detection Started..!!")
            print("Table Occupancy Check Started..!!")
            break;
        else:
            print("Please enter a valid restaurant number")


# MQTT Topic Names
topic_customer_details = "Restaurant/*/Customer_Data/Entry_Details/"
topic_customer_detection = "Restaurant/*/Customer_Detection"
topic_customer_handdetection = "Restaurant/*/Customer_HandDetection"

GPIO.setwarnings(False)
sensor=Adafruit_DHT.DHT11

# Certificates for AWS IOT Services
awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"   
awsport = 8883
caPath = "/home/pi/Public/Team_16_Project/Certificates/AmazonRootCA1.pem"
certPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-private.pem.key"
 
myclient = mqtt.Client("Sensor_Data_Publisher_Subscriber")
myclient.on_connect = on_connect
myclient.on_message = on_message
myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)
myclient.loop_start()
# Delay needed for connection
time.sleep(0.1)

try:
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER_IN = [3, 7, 8, 13, 16] # PI - Sensor
    PIN_ECHO_OUT = [5, 11, 10, 15, 18] # Sensor - PI
    TEMPERATURE_PIN = 7
    ENTRY_ACCEPTED = 32
    ENTRY_DENIED = 33
    LED_TABLE1_OUT = 35
    LED_TABLE2_OUT = 37
    LED_TABLE3_OUT = 31
    BUZZER_OUT = 40
    GPIO.setup(PIN_TRIGGER_IN, GPIO.OUT)
    GPIO.setup(PIN_ECHO_OUT, GPIO.IN)
    GPIO.setup(ENTRY_ACCEPTED,GPIO.OUT)
    GPIO.setup(ENTRY_DENIED,GPIO.OUT)
    GPIO.setup(LED_TABLE1_OUT, GPIO.OUT)
    GPIO.setup(LED_TABLE2_OUT, GPIO.OUT)
    GPIO.setup(LED_TABLE3_OUT, GPIO.OUT)
    GPIO.setup(BUZZER_OUT, GPIO.OUT)
    valid_restaurant_location()
    valid_restaurant_number()
    
    t0 = threading.Thread(target=customer_entry_details,args=[PIN_TRIGGER_IN[0],PIN_ECHO_OUT[0],0.1,TEMPERATURE_PIN],daemon=True)
    t0.start()
    t1 = threading.Thread(target=subscriber_start,args=[topic_customer_details],daemon=True)
    t1.start()
    t2 = threading.Thread(target=customer_presence_table_data,args=[PIN_TRIGGER_IN[1],PIN_ECHO_OUT[1],0.15,PIN_TRIGGER_IN[2],PIN_ECHO_OUT[2],0.2,PIN_TRIGGER_IN[3],PIN_ECHO_OUT[3],0.3],daemon=True)
    t2.start()
    t3 = threading.Thread(target=customer_movement_hand_detection,args=[PIN_TRIGGER_IN[4],PIN_ECHO_OUT[4],0.4],daemon=True)
    t3.start()
    t4 = threading.Thread(target=subscriber_start,args=[topic_customer_detection],daemon=True)
    t4.start()
    t5 = threading.Thread(target=subscriber_start,args=[topic_customer_handdetection],daemon=True)
    t5.start()
    t6 = threading.Thread(target=writeToFirebase,args=[],daemon=True)
    t6.start()
    
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Close")

    






