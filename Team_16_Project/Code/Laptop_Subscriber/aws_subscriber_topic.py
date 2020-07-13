#!/usr/bin/python
import ssl
import time
import json
import paho.mqtt.client as mqtt
import base64
import threading
import requests
import sys
import os
from firebase import firebase
from datetime import date
import sys, os

# Function for Image Reconstructio and Mask detection output
def mask_detection(image_data_str):
    image_data = image_data_str.encode('utf-8')                                                                                                                 
    image_64_decode = base64.decodebytes(image_data)                                                            
    image_result = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/result.jpg", "wb+") 
    image_result.write(image_64_decode)
    image_result.close()
    os.system("python3 detect_mask_image.py --image /Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/result.jpg > /dev/null 2>&1")
    file_result=open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/mask_output.txt", "r")
    mask_output=file_result.read(1)
    return mask_output
    
# Function for Receiving Customer ID Check status from DataBase
def customer_id_check(database_input):
    if(int(database_input) == 1):
        id_check_ai_input = 0
    else:
        id_check_ai_input = 1

    file_result_customer_id = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/Customer_Status_output.txt","a")
    file_result_customer_id.write(str(id_check_ai_input))
    file_result_customer_id.close() 
    time.sleep(1)
    start_AI_plan()  

# Function for Customer Temperature Check
def body_temperature_check(body_temperature):
    if(int(body_temperature) <= int(maximum_body_temperature)):
        body_temperature_output = 1
    else:
        body_temperature_output = 0
    return body_temperature_output

locationToId =	{
  "Stuttgart": "0",
  "Boblingen": "1",
  "Esslingen": "2",
  "Ludwigsburg": "3"
}

idToLocation =	{
  "0": "Stuttgart",
  "1": "Boblingen",
  "2": "Esslingen",
  "3": "Ludwigsburg"
}

# Function to evaluate the results of Customer Entry
def customer_entry_details(input_restaurant_location, input_restaurant_number, input_customer_image,input_temperature_value):
    temperature_ai_input = body_temperature_check(input_temperature_value)    
    mask_ai_input = mask_detection(input_customer_image)
    file_result = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/Customer_Status_output.txt", "w+")
    file_result.write(locationToId[input_restaurant_location] + input_restaurant_number +
                      str(temperature_ai_input) + str(mask_ai_input))
    file_result.close()

# Function to return True / False
def True_False(input_value):
    if(input_value == str(1)):
        result = True
    else:
        result = False
    return result

def start_AI_plan():
    file_reading_ai_input()
    ai_plan_output()

# Function for giving the input to Problem file Generator and calling AI Plan
def file_reading_ai_input():
    file_reading = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/Customer_Status_output.txt","r")
    file_result = file_reading.read(5)
    temperature_problem_file_input = True_False(file_result[2])
    mask_problem_file_input = True_False(file_result[3])
    customer_id_problem_file_input = True_False(file_result[4])
    GenerateProblemPDDLFile(mask_problem_file_input,customer_id_problem_file_input,temperature_problem_file_input)
    GetAIPlan()

# Function for Generating Problem file
def GenerateProblemPDDLFile(MaskSensor, IDSensor, TempSensor):
	ProbFile = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/SSSR_ProblemFile.pddl","w+")
	ProbFile.write("(define\n\n(problem SSSR_CustomerAcceptance)\n\n(:domain SSSR)\n\n(:objects\tMask - mask\n\t\tID - RFID\n\t\tTemperature - temp\n\t\tMainDoor - door\n\t\tCustomer Manager - person\n)\n\n")
	ProbFile.write("(:init\t(IsCustomer Customer)\n\t\t(IsManager Manager)\n\t\t(IsDoor MainDoor)\n")
	if(MaskSensor == True):
		ProbFile.write("\t\t(MaskOkay Mask)\n")
	if(IDSensor == True):
		ProbFile.write("\t\t(HealthOkay ID)\n")
	if(TempSensor == True):
		ProbFile.write("\t\t(TempOkay Temperature)\n")
	ProbFile.write(")\n\n")
	ProbFile.write("(:goal\t(and (JudgeCustomer Customer)(not (IsDoorOpen MainDoor))(not (ManagerAlert Manager)) )\n) \n\n)")

# Function to generate AI Plan     
def GetAIPlan():
	data = {'domain': open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/SSSR_DomainFile.pddl", 'r').read(),
    'problem' : open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/SSSR_ProblemFile.pddl", 'r').read()}
	response = requests.post('http://solver.planning.domains/solve', json = data).json()
	with open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/AIPlan.txt", 'w') as f:
		for act in response['result']['plan']:
			f.write(str(act['name']))
			f.write('\n')  

# Function for reading the output of AI Plan 
def ai_plan_output():
    ai_plan_output_file_read = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/AIPlan.txt", 'r')
    output = ai_plan_output_file_read.read()
    first_word = str(output.split()[0])
    print("AI Planner Output : " + first_word[1:])
    actuation_data_send(first_word)

totalCustomerCount = [0, 0, 0 , 0]
allowedCustomerCount = [0,0,0,0]
safenessLevelList = ["NoRisk","NoRisk","NoRisk","NoRisk"]
locationToRestaurantTableMap = [[4,4,4,4],[4,4,4,4],[4,4,4,4],[4,4,4,4],[4,4,4,4]]

# Function for sending customer_check result
def actuation_data_send(input_ai_plan_data):
    file_reading = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/AI_Planning/Customer_Status_output.txt","r")
    file_result = file_reading.read(2)
    totalCustomerCount[int(file_result[0])] = totalCustomerCount[int(file_result[0])] + 1

    if input_ai_plan_data.find("reject") == 1:
        customer_data_output = 0
    elif input_ai_plan_data.find("allow") == 1:
        customer_data_output = 1
        allowedCustomerCount[int(file_result[0])] = allowedCustomerCount[int(file_result[0])] + 1
    else:
        print("No output from AI Planning")
        customer_data_output = 0
    payload_customer_data = {"Customer_Entry_Result":customer_data_output}
    publisher_data(topic_customer_details,payload_customer_data)
    writeToAppDatabase(file_result[0], file_result[1], totalCustomerCount[int(file_result[0])], allowedCustomerCount[int(file_result[0])])
    writeAiPlanningToFirebase(file_result[0], file_result[1], input_ai_plan_data)

# Method writes the Available seats and safenessLevel of the location to database
def writeToFirebase(location, id, safenessLevel):
    firebase1 = firebase.FirebaseApplication('https://iotfirebase-d312f.firebaseio.com/', None)
    locationStr = idToLocation[location]
    locationIdVal = int(location)
    idVal = int(id)
    availableSeatsStr = str(locationToRestaurantTableMap[locationIdVal][idVal])
    data1 = {
             'RestaurantName': id,
             'AvailableTables': availableSeatsStr,
             'SafenessLevel': safenessLevel
             }
    firebase1.post("location/" + locationStr + "/" + date.today().strftime('%d-%m-%Y'), data1)

customerCount = [1, 1, 1, 1]

# Method writes the AIPlanner output to database
def writeAiPlanningToFirebase(locationId, restaurantId, aiOutput):
    firebase2 = firebase.FirebaseApplication('https://sssrprojectalldata.firebaseio.com/', None)
    locationStr = idToLocation[locationId]
    aiOutputStr = aiOutput[1:]
    data1 = {
             'RestaurantName': restaurantId,
             'CustomerId': str(customerCount[int(locationId)]),
             'AllowRejectReason': aiOutputStr
             }
    firebase2.post("location/" + locationStr + "/" + date.today().strftime('%d-%m-%Y'), data1)
    customerCount[int(locationId)] = customerCount[int(locationId)] + 1

# Method calculates the safeness level by taking total and allowed customers count
def writeToAppDatabase(location, id, totalCustomerCountVal,  allowedCustomerCountVal):
    print ( "TotalCustomerTested : "+str(totalCustomerCountVal) + " AllowedCustomers : "+ str(allowedCustomerCountVal))
    safeness_level = allowedCustomerCountVal / totalCustomerCountVal
    if (safeness_level < 0.2):
        safenessLevelList[int(location)] = "SevereRisk"
    elif (safeness_level < 0.5):
        safenessLevelList[int(location)] = "HighRisk"
    elif (safeness_level < 0.8):
        safenessLevelList[int(location)] = "ModerateRisk"
    else:
        safenessLevelList[int(location)] = "NoRisk"

    writeToFirebase(location, id, safenessLevelList[int(location)])

# Function for Hand Movement Check of Customer
def customer_handdetection_check(input_distance):
    if (int(input_distance) <= int(maximum_handdetection_distance)):
        buzzer_status = 1
        payload_buzzer_data = {"Buzzer_Status": buzzer_status}
        publisher_data(topic_customer_handdetection, payload_buzzer_data)

def customer_presence_table_check(location, id, distanceList):
    locationVal = int(locationToId[location])
    idVal = int(id)
    previousVal = locationToRestaurantTableMap[locationVal][idVal]
    locationToRestaurantTableMap[locationVal][idVal] = 3
    for i, distance in enumerate(distanceList):
        if (float(distance) <= float(maximum_distance)):
            if (locationToRestaurantTableMap[locationVal][idVal] > 0):
                locationToRestaurantTableMap[locationVal][idVal] = locationToRestaurantTableMap[locationVal][idVal] - 1
            led_state = 0
        else:
            if (locationToRestaurantTableMap[locationVal][idVal] < 3):
                locationToRestaurantTableMap[locationVal][idVal] = locationToRestaurantTableMap[locationVal][idVal] + 1
            led_state = 1
        payload_led_state = {"Table_Number_Output": i + 1, "Disinfectant_Status": led_state}
        publisher_data(topic_customer_detection, payload_led_state)

    if (previousVal != locationToRestaurantTableMap[locationVal][idVal]):
        writeToFirebase(locationToId[location], id, safenessLevelList[locationVal])


# Function to start subscriber based on topic
def subscriber_start(input_topic):
    while True:
        receiver.subscribe(input_topic,0)
        time.sleep(1)
    
# Function to call publisher to send data 
def publisher_data(input_topic_name,payload_data):
    publish_data = json.dumps(payload_data,indent = 4)
    receiver.publish(input_topic_name,publish_data,0)
    time.sleep(0.1)

# on_connect callback
def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

#on_message callback
def on_message(client, userdata, msg):    
    if(msg.topic == topic_customer_details):
        payload_data = json.loads(msg.payload)
        customer_entry_details(payload_data["Location"], payload_data["Restaurant_number"],
                               payload_data["Face_Image"],payload_data["Body_Temperature"])
    elif (msg.topic == topic_hospital_database):
        payload_data = json.loads(msg.payload)
        customer_id_check(payload_data["DataBase_result"])
    elif (msg.topic == topic_customer_detection):
        payload_data = json.loads(msg.payload)
        tableListDistance = [str(payload_data["Distance_Table1"]), str(payload_data["Distance_Table2"]), str(payload_data["Distance_Table3"])]
        customer_presence_table_check(payload_data["Location"], payload_data["Restaurant_number"], tableListDistance)
        
    elif (msg.topic == topic_customer_handdetection):
        payload_data = json.loads(msg.payload)
        customer_handdetection_check(payload_data["Distance"])
    else:
        print("Not a valid topic")
        
# AWS IOT certificates       
userdata= "Sensor_Data_Receiver"
awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"  
awsport = 8883

caPath = "/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/Certs/AmazonRootCA1.pem"
certPath = "/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/Certs/0b5fd75186-certificate.pem.crt"
keyPath = "/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/Certs/0b5fd75186-private.pem.key"

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
topic_customer_details = "Restaurant/*/Customer_Data/Entry_Details/"
topic_customer_detection = "Restaurant/*/Customer_Detection"
topic_customer_handdetection = "Restaurant/*/Customer_HandDetection"
topic_hospital_database = "Restaurant/Hospital_Database/Customer_ID_Status"

t0 = threading.Thread(target=subscriber_start,args=[topic_hospital_database])
t0.start()

t1 = threading.Thread(target=subscriber_start,args=[topic_customer_details])
t1.start()

t2 = threading.Thread(target=subscriber_start,args=[topic_customer_detection])
t2.start()

t3 = threading.Thread(target=subscriber_start,args=[topic_customer_handdetection])
t3.start()

t0.join()
t1.join()
t2.join()
t3.join()


    
    
    
    
