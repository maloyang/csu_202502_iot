
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import requests
import csv
import folium
import geocoder

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/test')
def test():
    return 'test for flask'

@app.route('/map_demo')
def map_demo():
    url = "https://raw.githubusercontent.com/maloyang/KH20221202_IoT_Data_Science/main/W01/bike_02_新北市.csv"
    r = requests.get(url)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data_list = list(cr)

    # 使用 geocoder 取得特定住址的 GPS 座標
    #location = geocoder.osm('新北市').latlng
    location = (data_list[1][6], data_list[1][7])

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

    # 將 Folium 地圖物件轉換為 HTML 字串
    map_html = m._repr_html_()
    return map_html
