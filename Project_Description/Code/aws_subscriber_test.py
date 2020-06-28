#!/usr/bin/python

import ssl
import time
import json
import paho.mqtt.client as mqtt
import base64

def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):
    image_64_decode = base64.decodebytes(msg.payload) 
    image_result = open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/result.jpg", "wb") # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    


    
userdata="smartcityiot"
awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"  
awsport = 8883

caPath = "/home/pi/Downloads/AmazonRootCA1.pem"
certPath = "/home/pi/Downloads/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Downloads/0b5fd75186-private.pem.key"

receiver = mqtt.Client(userdata)
receiver.on_connect = on_connect 
receiver.on_message = on_message

receiver.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
receiver.connect(awshost, awsport, keepalive=60)
receiver.loop_start()



while True:
    
    receiver.subscribe("publishdata/info",0)
    time.sleep(1)

    
    
    
    
    
    
