import configparser

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route("/results", methods=['POST'])
def render_results():
    print( "Results")
    zip_code = request.form['zip_code']
    country = request.form['country']
    print(zip_code, country)
    return {zip_code: "Zip Code: " + str(zip_code), 'country': 'Country: ' + str(country)}


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config['openweathermap']['API_KEY']


def get_weather_results(zip_code, country_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}".format(zip_code, country_code, api_key)
    print(api_url)
    response = requests.get(api_url)
    return response.json()


if __name__ == '__main__':
    app.run()
    # print(get_weather_results("87000", 'FR', get_api_key()))
