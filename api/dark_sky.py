import pandas as pd
from pandas.io.json import json_normalize
import requests


class DarkSkyWeatherForecast(object):
    def __init__(self, latitude, longitude, api_key):
        self.lat = latitude
        self.lon = longitude
        self.key = api_key
        self.freqs = ['minutely', 'hourly', 'daily']
        try:
            url = 'https://api.darksky.net/forecast/{}/{},{}?units=si'.format(api_key, latitude, longitude)
            response = requests.get(url)
            json_response = response.json()
            self.forecast = json_response
            self.observation = json_normalize(self.forecast['currently'])
            self.observation.index = pd.to_datetime(self.observation['time'], unit='s')
            self.daily = json_normalize(self.forecast['daily']['data'])
            self.daily.index = pd.to_datetime(self.daily['time'], unit='s')
            self.daily.summary = self.forecast['daily']['summary']
            self.hourly = json_normalize(self.forecast['hourly']['data'])
            self.hourly.index = pd.to_datetime(self.hourly['time'], unit='s')
            self.hourly.summary = self.forecast['hourly']['summary']
            self.minutely = json_normalize(self.forecast['minutely']['data'])
            self.minutely.index = pd.to_datetime(self.minutely['time'], unit='s')
            self.minutely.summary = self.forecast['minutely']['summary']
        except Exception as e:
            print(e)
