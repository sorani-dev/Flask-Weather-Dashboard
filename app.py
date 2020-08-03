import requests
import configparser
import os

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
    print(get_weather_results("87000", 'FR', get_api_key()))
