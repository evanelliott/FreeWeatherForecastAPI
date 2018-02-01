from urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize


class WeatherForecastOWM(object):
    def __init__(self, latitude=51.8043, longitude=-0.8058, api_key='74f76fb377ca093fe33fa60a00d8bf90'):
        self.lat = latitude
        self.lon = longitude
        self.key = api_key
        # get 5 day (3hrly) forecast
        try:
            url_three_hourly_fc = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}'.format(
                                                           latitude, longitude, api_key)
            json_three_hourly_fc = json.loads(urlopen(url_three_hourly_fc).read())
            self.fc_latitude = json_three_hourly_fc['city']['coord']['lat']
            self.fc_longitude = json_three_hourly_fc['city']['coord']['lon']
            self.forecast_three_hourly = json_normalize(json_three_hourly_fc['list'])
            self.forecast_three_hourly.index = pd.to_datetime(self.forecast_three_hourly['dt'], unit='s')
        except Exception as e:
            print(e)
        # get current observation
        try:
            url_current = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID={}'.format(
                latitude, longitude, api_key)
            json_current = json.loads(urlopen(url_current).read())
            self.current_observation = pd.io.json.json_normalize(json_current)
            self.current_observation.index = pd.to_datetime(self.current_observation['dt'], unit='s')
            self.ob_latitude = json_current['coord']['lat']
            self.ob_longitude = json_current['coord']['lon']
        except Exception as e:
            print(e)
        pass


if __name__ == '__main__':
    wf = WeatherForecastOWM()
    print(wf.current_observation)
    print(wf.forecast_three_hourly)
