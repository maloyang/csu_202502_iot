import paho.mqtt.client as mqtt
import time, json, datetime, sys, os

temp_list = []
client2 = None
#==================
#== MQTT Functions

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時 
    # 地端程式將會重新訂閱
    client.subscribe('/fc6b2f9438/farm2/B7/v3')
    client.subscribe('/fc6b2f9438/farm2/B2/temp')
    client.subscribe('/fc6b2f9438/farm2/B2/humi')
    client.subscribe('/fc6b2f9438/farm2/B2/CO2')
    
    

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    try:
        topic = msg.topic
        value = msg.payload.decode('utf-8')
        dtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('(topic, value)=(%s, %s) @%s' %(topic, value, dtime))

        # push data
        topic2 = '/csu2021/farm/' + topic.split('/')[-1]
        client2.publish(topic2, value)
        print('push to :', topic2, value)

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
        client.connect("mqtt.ewxew.com", 1883, 60)

        # 開始連線，執行設定的動作和處理重新連線問題
        # 也可以手動使用其他loop函式來進行連接
        #client.loop_forever()
        client.loop_start()    #start the loop

        '''
        time.sleep(30)

        client.disconnect() # disconnect gracefully
        client.loop_stop() # stops network loop
        '''

    except Exception as e:
        print('run mqtt error: ', str(e))

def run_mqtt2():
    global client2
    try:
        # 連線設定
        # 初始化地端程式
        client2 = mqtt.Client()

        # 設定連線的動作
        client2.on_connect = on_connect

        # 設定接收訊息的動作
        client2.on_message = on_message

        # 設定登入帳號密碼
        #client.username_pw_set("try","xxxx")

        # 設定連線資訊(IP, Port, 連線時間)
        client2.connect("broker.hivemq.com", 1883, 60)

        # 開始連線，執行設定的動作和處理重新連線問題
        # 也可以手動使用其他loop函式來進行連接
        #client.loop_forever()
        client2.loop_start()    #start the loop

        '''
        time.sleep(30)

        client.disconnect() # disconnect gracefully
        client.loop_stop() # stops network loop
        '''
        
    except Exception as e:
        print('run mqtt error: ', str(e))

run_mqtt2()
run_mqtt()

while True:
    pass
