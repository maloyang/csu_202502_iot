# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, send_file
import requests
import csv
import folium
import geocoder

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name:
        return 'Hello! %s~' %(name)

    return 'Hello! Malo~'


@app.route('/hello/html')
def hello_html():
    html = '''<h1>你好</h1>
                <p style="background:red;"> malo's web site</p>'''
    return html


@app.route('/map/demo1')
def map_demo1():
    url = "https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/csv/file"
    r = requests.get(url)
    print(r)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data_list = list(cr)

    # 使用 geocoder 取得特定住址的 GPS 座標
    location = geocoder.osm('新北市').latlng

    m = folium.Map(location=location, zoom_start=14)

    for item in data_list[1:]:
        try:
            name = item[1]
            area = item[4]
            total = item[2]
            n = item[3]
            lat = item[6]
            lng = item[7]
            if int(n)<5 and int(n)>0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='red', prefix='fa', icon='fa-bicycle')).add_to(m)
            elif int(n)==0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='black', prefix='fa', icon='fa-bicycle')).add_to(m)
            else:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='green', prefix='fa', icon='fa-bicycle')).add_to(m)
            
        except Exception as e:
            print(e.args)    

    m.save('map1.html')
                
    return send_file('./map1.html')



@app.route('/map/demo2')
def map_demo2():
    url = "https://raw.githubusercontent.com/maloyang/KH20221202_IoT_Data_Science/main/W01/bike_02_新北市.csv"
    r = requests.get(url)
    print(r)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data_list = list(cr)

    # 使用 geocoder 取得特定住址的 GPS 座標
    location = geocoder.osm('新北市').latlng

    m = folium.Map(location=location, zoom_start=14)

    for item in data_list[1:]:
        try:
            name = item[1]
            area = item[4]
            total = item[2]
            n = item[3]
            lat = item[6]
            lng = item[7]
            if int(n)<5 and int(n)>0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='red', prefix='fa', icon='fa-bicycle')).add_to(m)
            elif int(n)==0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='black', prefix='fa', icon='fa-bicycle')).add_to(m)
            else:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='green', prefix='fa', icon='fa-bicycle')).add_to(m)
            
        except Exception as e:
            print(e.args)    

    m.save('map1.html')
                
    return send_file('./map1.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8100)
