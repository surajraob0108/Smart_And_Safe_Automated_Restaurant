#!/usr/bin/python
import RPi.GPIO as GPIO
import Python_DHT
import datetime
import time
import os
import socket
import ssl
import paho.mqtt.client as mqtt
sensor = Python_DHT.DHT11

    

awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"   
awsport = 8883
#clientid = "Team_16_IOT" #Thing name
#thingName = "Team_16_SC_IOT"
caPath = "/home/pi/Downloads/AmazonRootCA1.pem"
certPath = "/home/pi/Downloads/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Downloads/0b5fd75186-private.pem.key"

myclient = mqtt.Client('ssbtx')

myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)
myclient.loop_start()

pin = 7 # PIN 26
GPIO.setmode(GPIO.BOARD)
while True:
    humidity, temperature = Python_DHT.read_retry(sensor, pin)     
    print("Temperature = "+str(temperature))
    temperature = '{"Temperature": '+'"'+str(temperature)+'"}'
    myclient.publish("publishdata/info", temperature, 0)
    time.sleep(3)
    
    
    
    
    
    
    
