from urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize


class WeatherForecastWU(object):
    def __init__(self, latitude=51.8043, longitude=-0.8058, api_key='11b99091b788481f'):
        self.lat = latitude
        self.lon = longitude
        self.key = api_key
        try:
            json_response = json.loads(urlopen('http://api.wunderground.com/api/{}/{}/q/{},{}.json'.format(
                api_key, 'alerts/conditions/forecast10day/hourly10day', latitude, longitude)).read())
            self.current_observation = json_normalize(json_response['current_observation'])
            self.current_observation.index = pd.to_datetime(self.current_observation['observation_epoch'], unit='s')
            self.forecast_simple = json_normalize(json_response['forecast']['simpleforecast']['forecastday'])
            self.forecast_simple.index = pd.to_datetime(self.forecast_simple['date.epoch'], unit='s')
            self.forecast_text = json_normalize(json_response['forecast']['txt_forecast']['forecastday'])  # would need to be converted to degC
            self.forecast_hourly = json_normalize(json_response['hourly_forecast'])
            self.forecast_hourly.index = pd.to_datetime(self.forecast_hourly['FCTTIME.epoch'], unit='s')
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    wf = WeatherForecastWU()
    print(wf.current_observation)
    print(wf.forecast_hourly)
