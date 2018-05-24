import configparser
import pandas as pd


def get_locations():
    return pd.read_csv('config/locations.csv', index_col='LocationID')


def get_forecast_metadata():
    c = configparser.ConfigParser()
    c.read('config/forecast_metadata.ini')
    forecast_metadata = dict()
    for key in c._sections['DarkSkyForecastFeatures'].keys():
        forecast_metadata[key] = c.get('DarkSkyForecastFeatures', key).split(',')
    return forecast_metadata


def get_credentials():
    c = configparser.ConfigParser()
    c.read('config/credentials.ini')
    credentials = {}
    for key in c._sections['Credentials'].keys():
        credentials[key] = c.get('Credentials', key)
    return credentials
