from flask import Flask # <--- 引入 Flask

app = Flask(__name__)

@app.route('/')
def home():
    # etc etc, flask app code
    return "hello, home"


if __name__ == '__main__':
    app.run()