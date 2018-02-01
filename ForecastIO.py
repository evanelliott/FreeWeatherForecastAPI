from urllib.request import urlopen
import pandas as pd
from pandas.io.json import json_normalize


class WeatherForecastFIO(object):
    def __init__(self, latitude=51.8043, longitude=-0.8058, api_key='7e447c401e146ee063128b9b21506f74'):
        self.lat = latitude
        self.lon = longitude
        self.key = api_key
        try:
            json_response = json.loads(urlopen('https://api.darksky.net/forecast/{}/{},{}'.format(
                api_key, latitude, longitude)).read())
            self.forecast = json_response
            self.current_observation = json_normalize(self.forecast.json['currently'])
            self.current_observation.index = pd.to_datetime(self.current_observation['time'], unit='s')
            self.forecast_daily = json_normalize(self.forecast.json['daily']['data'])
            self.forecast_daily.index = pd.to_datetime(self.forecast_daily['time'], unit='s')
            self.forecast_daily.summary = self.forecast.json['daily']['summary']
            self.forecast_hourly = json_normalize(self.forecast.json['hourly']['data'])
            self.forecast_hourly.index = pd.to_datetime(self.forecast_hourly['time'], unit='s')
            self.forecast_hourly.summary = self.forecast.json['hourly']['summary']
            self.forecast_minutely = json_normalize(self.forecast.json['minutely']['data'])
            self.forecast_minutely.index = pd.to_datetime(self.forecast_minutely['time'], unit='s')
            self.forecast_minutely.summary = self.forecast.json['minutely']['summary']
        except Exception as e:
            print(e)


if __name__ == '__main__':
    wf = WeatherForecastFIO()
    print(wf.current_observation)
    print(wf.forecast_hourly)
