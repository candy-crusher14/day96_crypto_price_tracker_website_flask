from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


app.jinja_env.filters['to_float'] = to_float


def GetCryptoData():
    url = "https://api.coincap.io/v2/assets"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


@app.route('/')
def homepage():
    data = GetCryptoData()
    if data:
        return render_template('front_webpage.html', cryptos=data)
    else:
        return render_template('timeout.html',
                               error_message="Failed to retrieve cryptocurrency data. Please try again later.")




if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)


