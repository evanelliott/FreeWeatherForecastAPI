from urllib.request import urlopen
import pandas as pd
from pandas.io.json import json_normalize
import json


class WeatherForecastFIO(object):
    def __init__(self, latitude=51.8043, longitude=-0.8058, api_key='7e447c401e146ee063128b9b21506f74'):
        self.lat = latitude
        self.lon = longitude
        self.key = api_key
        self.freqs = ['minutely', 'hourly', 'daily']
        try:
            json_response = json.loads(urlopen('https://api.darksky.net/forecast/{}/{},{}'.format(
                api_key, latitude, longitude)).read())
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


if __name__ == '__main__':
    wf = WeatherForecastFIO()
    print(wf.observation)
    print(wf.minutely)
    print(wf.hourly)
    print(wf.daily)
