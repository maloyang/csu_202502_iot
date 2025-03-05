import paho.mqtt.client as mqtt
import time, json, datetime, sys, os

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import time
from struct import *
import random

topic_light = '/csu2023/light'
#==================
#== MQTT Functions

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe(topic_light)
    

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    try:
        topic = msg.topic
        value = msg.payload.decode('utf-8')
        dtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('(topic, value)=(%s, %s) @%s' %(topic, value, dtime))
        if topic == topic_light:
            if value=='1':
                control_light(1)
            else:
                control_light(0)

    except Exception as e:
        print('read data exception: ', str(e))

def run_mqtt():
    try:
        # 連線設定
        # 初始化地端程式
        client = mqtt.Client()

        # 設定連線的動作
        client.on_connect = on_connect

        # 設定接收訊息的動作
        client.on_message = on_message

        # 設定登入帳號密碼
        #client.username_pw_set("try","xxxx")

        # 設定連線資訊(IP, Port, 連線時間)
        client.connect("broker.hivemq.com", 1883, 60)

        # 開始連線，執行設定的動作和處理重新連線問題
        # 也可以手動使用其他loop函式來進行連接
        #client.loop_forever()
        client.loop_start()    #start the loop


        #time.sleep(30)
        while True:
            pass

        client.disconnect() # disconnect gracefully
        client.loop_stop() # stops network loop
        
    except Exception as e:
        print('run mqtt error: ', str(e))

#========================
# modbus io function
mbComPort = 'COM7' # for linux: '/dev/ttyUSB0'
baudrate = 9600
databit = 8
parity = 'N'
stopbit = 1
mbTimeout = 100 # ms

def control_light(value):
    mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
    master = modbus_rtu.RtuMaster(mb_port)
    master.set_timeout(mbTimeout/1000.0)

    mbId = 1
    addr = 0

    try:
        #-- FC5: write multi-coils
        rr = master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=value)
        print("Write(addr, value)=%s" %(str(rr)))

    except Exception as e:#Exception, e:
        print("modbus test Error: " + str(e))

    master._do_close()


run_mqtt()
