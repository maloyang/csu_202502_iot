import requests
import folium
import pandas as pd
from flask import Flask

app = Flask(__name__)

def visualize_pm25_v4():
    """
    抓取新的 PM2.5 資料並使用 Folium 視覺化 (使用測站經緯度)，再次修正 PM2.5 欄位名稱。
    """
    url = "https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=9e565f9a-84dd-4e79-9097-d403cae1ea75&limit=1000&sort=ImportDate%20desc&format=JSON"

    try:
        response = requests.get(url)
        data = response.json().get('records')

        if not data:
            return "<p style='color:orange;'>無法從 API 獲取有效的 'records' 資料，請檢查 API 回應或稍後再試。</p>"

        df = pd.DataFrame(data)
        required_columns = ['sitename', 'longitude', 'latitude', 'pm2.5']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f"<p style='color:red;'>資料中缺少必要的欄位：{', '.join(missing_columns)}</p>"

        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['pm2.5'] = pd.to_numeric(df['pm2.5'], errors='coerce')
        df_cleaned = df.dropna(subset=['latitude', 'longitude', 'pm2.5'])

        if df_cleaned.empty:
            return "<p style='color:orange;'>經過清理後，沒有有效的 PM2.5 資料點可以顯示。可能是原始資料品質問題或 PM2.5 數值缺失。</p>"

        center_lat = df_cleaned['latitude'].mean()
        center_lon = df_cleaned['longitude'].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

        for index, row in df_cleaned.iterrows():
            station_name = row['sitename']
            latitude = row['latitude']
            longitude = row['longitude']
            pm25_value = row['pm2.5']
            color = 'green'
            popup_text = f"測站名稱: {station_name}<br>PM2.5: {pm25_value}"
            if pm25_value > 54: color = 'purple'
            elif pm25_value > 35: color = 'red'
            elif pm25_value > 25: color = 'orange'
            elif pm25_value > 15: color = 'yellow'
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=f"{station_name}: PM2.5 = {pm25_value}",
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(m)
        map_html = m._repr_html_()
        return map_html
    except requests.exceptions.RequestException as e:
        return f"<p style='color:red;'>抓取資料時發生網路錯誤：{e}</p>"
    except KeyError as e:
        return f"<p style='color:red;'>處理 JSON 資料時發生鍵錯誤 (KeyError)，可能是 API 回應格式有變：{e}</p>"
    except Exception as e:
        return f"<p style='color:red;'>發生未預期的錯誤：{e}</p>"


@app.route('/')
def home():
    # etc etc, flask app code
    return "hello, home"

@app.route('/test')
def test():
    # etc etc, flask app code
    return "hello, test"

@app.route('/map')
def map():
    # etc etc, flask app code
    return visualize_pm25_v4()


if __name__ == '__main__':
    app.run()