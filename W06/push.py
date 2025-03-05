# push mqtt msg

import paho.mqtt.client as mqtt
import time, json, datetime, sys, os
import random

def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+", result code "+str(rc)+", client_id  "+str(client)
    print(m)

# some online free broker:
#   iot.eclipse.org
#   test.mosquitto.org
#   broker.hivemq.com
broker_address = "broker.hivemq.com"
broker_port = 1883

client1 = mqtt.Client()    #create new instance
client1.on_connect = on_connect        #attach function to callback

time.sleep(0.5)
client1.connect(host=broker_address, port=broker_port, keepalive=60)      #connect to broker
topic_str = '/csu2023/temp'
        
client1.loop_start()    #start the loop
time.sleep(0.5)
print("loop start")

#-- start to push data
for k in range(1000):
    temp = 25 + random.randint(-3, 5)
    print('--> push', topic_str, temp)
    client1.publish(topic_str, temp, qos=1)
    time.sleep(5)

time.sleep(0.1)

client1.disconnect()
