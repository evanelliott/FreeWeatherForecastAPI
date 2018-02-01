from urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize


def get_location_code(search_name, api_key='EKP3jy3P1KI7p1ad4vGVk72LVaEq3qKv'):
    search_results = json.loads(
        urllib2.urlopen('http://apidev.accuweather.com/locations/v1/search?q={}&apikey={}'.format(
            search_name, 'hoArfRosT1215')).read())
    print('Found {} results.'.format(len(search_results)))
    results_df = json_normalize(search_results)
    print('Top result: {}, {}, {}.'.format(results_df.loc[0, 'EnglishName'],
                                           results_df.loc[0, 'AdministrativeArea.EnglishName'],
                                           results_df.loc[0, 'Country.ID']))
    location_code = results_df.loc[0, 'Key']
    print('Location code:   {}'.format(location_code))
    return location_code


class WeatherForecastAW(object):
    def __init__(self, location_code=321825, api_key='EKP3jy3P1KI7p1ad4vGVk72LVaEq3qKv'):
        self.location_code = location_code
        self.key = api_key
        try:
            json_current_conditions = json.loads(urlopen('http://apidev.accuweather.com/currentconditions/v1/' +
                                                         '{}.json?language=en&apikey={}&metric=true'.format(
                                                             location_code,
                                                             'hoArfRosT1215')).read())  # parameter 'hoA....' to be replaced with api_key but currently does not grant access
            self.current_observations = json_normalize(json_current_conditions)
            self.current_observations.index = pd.to_datetime(self.current_observations['EpochTime'], unit='s')
            # json_hourly_forecast = json.loads(urlopen('http://apidev.accuweather.com/forecasts/v1/hourly/12hour/' +
            #                                           '{}.json?apikey={}'.format(location_code, 'hoArfRosT1215')).read())
            # self.forecast_hourly = json_normalize(json_hourly_forecast)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    loc_code = get_location_code('aylesbury')
    wf = WeatherForecastAW(location_code=loc_code)
    print(wf.current_observations)

# Notes: This forecast provider has some issues. Can't seem to load hourly forecast....
# Using 'hoA..' key returns error "Access Forbidden"; using my api_key returns error "Service Unavailable".
