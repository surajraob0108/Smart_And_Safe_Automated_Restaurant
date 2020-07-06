#!/usr/bin/python

import ssl
import time
import json
import paho.mqtt.client as mqtt
import base64
import os

def on_connect(client, userdata, flags, rc):
    print ("Connection status: {}".format(rc))

def on_message(client, userdata, msg):


    image_64_decode = base64.decodestring(msg.payload)
    image_result = open("/Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/Face_detection/Face-Mask-Detection/temp/mask.jpg", "wb") # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    image_result.close()
    os.system("python3 detect_mask_image.py --image /Users/phaniabhishek/Documents/studies/SEM2/IOT/Project/Face_detection/Face-Mask-Detection/temp/mask.jpg")


userdata="smartcityiot"
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



while True:

    receiver.subscribe("publishdata/info",0)
    time.sleep(1)