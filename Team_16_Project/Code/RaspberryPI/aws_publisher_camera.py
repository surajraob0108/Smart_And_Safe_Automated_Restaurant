#!/usr/bin/python
from PIL import Image
from resizeimage import resizeimage
import time
import os
import ssl
import paho.mqtt.client as mqtt
import base64

awshost = "a1nky7phv7yfno-ats.iot.eu-central-1.amazonaws.com"   
awsport = 8883
caPath = "/home/pi/Public/Team_16_Project/Certificates/AmazonRootCA1.pem"
certPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-certificate.pem.crt"
keyPath = "/home/pi/Public/Team_16_Project/Certificates/0b5fd75186-private.pem.key"

myclient = mqtt.Client('ssbtx')
myclient.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
myclient.connect(awshost, awsport, keepalive=60)

myclient.loop_start()
os.system("wget 192.168.0.103:8080/photo.jpg")
time.sleep(2)

with open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/photo.jpg", "r+b") as f:
    with Image.open(f) as image:
        cover = resizeimage.resize_cover(image, [200, 100])
        cover.save("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/photo_resize.jpg", image.format)
        
image_updated = open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/photo_resize.jpg", "rb")
image_read = image_updated.read()
image_64_encode = base64.encodebytes(image_read)
os.remove("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/photo.jpg")
os.remove("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/photo_resize.jpg")

for a in range(0,2):
    #data = '{"Image": '+'"'+str(value)+'"}' 
    myclient.publish("publishdata/info", image_64_encode, 0)
    time.sleep(3)
        
    
    
    
    
    
    
    
