import configparser
import datetime

import requests
from flask import Flask, render_template, request

"""
Functions
"""


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config['openweathermap']['API_KEY'])
    return config['openweathermap']['API_KEY'].strip("'")


def get_weather_results(zip_code, country_code, api_key, unit='', lang='en'):
    if unit != '':
        unit = "&units=" + str(unit) + ''

    if lang != '':
        lang = '&lang' + lang

    api_url = "https://api.openweathermap.org/data/2.5/weather?q={},{}{}&appid={}{}".format(zip_code, country_code,
                                                                                            unit,
                                                                                            api_key, lang)
    print('api_url:', api_url)
    response = requests.get(api_url)
    return response.json()


app = Flask(__name__)

"""
Routes
"""
# text_speed_en = "Speed"
# text_speed_fr = "Vitesse"
#
# table = "my Speed".maketrans(text_speed_en, text_speed_fr)
@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route("/results", methods=['POST'])
def render_results():
    # print("Results")
    # get the values to search from the user
    zip_code = request.form['zip_code']
    country = request.form['country']
    unit = request.form['unit']
    lang = request.form['lang']

    # if unit != '':
    #     unit = "&units=" + str(unit) + ''

    # print(zip_code, country, unit)

    # get the data from the API
    data = get_weather_results(zip_code=zip_code, country_code=country, api_key=get_api_key(), unit=unit, lang=lang)

    print(data)

    # parse data
    temp = "{0:.2f}".format(data['main']['temp'])
    feels_like = "{0:.2f}".format(data['main']['feels_like'])
    weather_short = data['weather'][0]['main']
    weather_desc = data['weather'][0]['description']
    wind = data['wind']
    location = data['name']
    # time_retreived = int(data['dt']).strftime("%b %d %Y %H:%M:%S"))
    time_retreived = datetime.datetime.utcfromtimestamp(int(data['dt'])).strftime("%b %d %Y %H:%M:%S")
    time_retreived_local = datetime.datetime.utcfromtimestamp(int(data['dt']) + int(data['timezone'])).strftime("%b %d %Y %H:%M:%S")


    if unit == '':
        unit = 'K'
    elif unit == 'metric':
        unit = 'C'
    else:
        unit = 'F'

    return render_template('results.html', location=location, temp=temp, feels_like=feels_like,
                           weather_short=weather_short, weather_desc=weather_desc, wind=wind,
                           time_retreived=time_retreived, time_retreived_local=time_retreived_local)

    return {zip_code: "Zip Code: " + str(zip_code), 'country': 'Country: ' + str(country), 'unit': 'Unit: ' + str(unit),
            'api_key': api_key}


if __name__ == '__main__':
    app.run()
    # print(get_weather_results("87000", 'FR', get_api_key()))
