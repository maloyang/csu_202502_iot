import requests
import folium
import gradio as gr
import pandas as pd
from flask import Flask # <--- 引入 Flask

app = Flask(__name__)

@app.route('/')
def home():
    # etc etc, flask app code
    return "hello, home"

@app.route('/test')
def test():
    # etc etc, flask app code
    return "hello, test"

if __name__ == '__main__':
    app.run()