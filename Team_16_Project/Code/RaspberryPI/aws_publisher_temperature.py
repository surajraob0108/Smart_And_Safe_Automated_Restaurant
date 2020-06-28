#!/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import ssl
import paho.mqtt.client as mqtt
sensor=Adafruit_DHT.DHT11
    

awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"   
awsport = 8883
caPath = "/home/pi/Public/Team_16_Project/Certificates/AmazonRootCA1.pem"
certPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-private.pem.key"

myclient = mqtt.Client("temperature_data")

myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)
myclient.loop_start()

pin = 7 # PIN 26
GPIO.setmode(GPIO.BOARD)
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print("Temperature = "+str(temperature))
    temperature = '{"Temperature": '+'"'+str(temperature)+'"}'
    myclient.publish("publishdata/info", temperature, 0)
    time.sleep(3)
    
    
    
    
    
    
    
