from ForecastIO import WeatherForecastFIO
from WUnderground import WeatherForecastWU
from OpenWeatherMap import WeatherForecastOWM
from AccuWeather import WeatherForecastAW
from readconfig import get_config
import sqlite3
import os
import pyodbc
import numpy as np
import pandas as pd
from urllib.request import urlopen

# Missing data for Stoke Park??


def _ping(url):
    urlopen(url)


def connect_to_db(db_name):
    conn = sqlite3.connect('{}.db'.format(db_name))
    print("\nConnected to database '{}'".format(db_name))
    return conn


class DataBasePreparer(object):
    def __init__(self, tables_metadata_dict):
        self.conn = None
        self.tables = tables_metadata_dict
        for db_name in tables_metadata_dict.keys():
            self.conn = connect_to_db(db_name)
            for tbl in tables_metadata_dict[db_name].keys():
                self.delete_table_if_exists(table_name=tbl)
                self.create_table(table_name=tbl, columns=tables_metadata_dict[db_name][tbl])
                print('Prepared table "{}"'.format(tbl))
            self.conn.close()

    def delete_table_if_exists(self, table_name):
        c = self.conn.cursor()
        query_to_delete_table = """DROP TABLE IF EXISTS {};""".format(table_name)
        c.execute(query_to_delete_table)
        self.conn.commit()

    def create_table(self, table_name, columns):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE {} ({})""".format(table_name, ', '.join([col.replace('.', '_') for col in columns])))
        self.conn.commit()


class DataHandler(object):
    def __init__(self, club_id):
        self.club_id = club_id
        self.data = self.get_forecasts(club_id)
        self.conn = None
        self.provider = None

    @staticmethod
    def get_forecasts(club_id):
        print('\n\nGetting data for id {}: {}'.format(club_id, club_metadata.loc[club_id, 'ClubName']))
        lat = club_metadata.loc[club_id, 'Latitude']
        lon = club_metadata.loc[club_id, 'Longitude']
        # location_code = club_metadata.loc[club_id, 'AccuWeatherLocation']

        return {'ForecastIO': WeatherForecastFIO(latitude=lat, longitude=lon),
                # 'WeatherUnderground': WeatherForecastWU(latitude=lat, longitude=lon),
                # 'OpenWeatherMap': WeatherForecastOWM(latitude=lat, longitude=lon)
                # Excluding Accuweather because it is unreliable
                # , 'AccuWeather': WeatherForecastAW(location_code=location_code)
                }

    def save_data_to_sql_table(self, input_data, table_name, table_columns):
        c = self.conn.cursor()
        data = getattr(input_data, table_name)
        desired_cols = [col for col in table_columns if col in data.columns]
        data = data[desired_cols]
        values = '"),\n("'.join(
            ['{}", "'.format(self.club_id) + '", "'.join([str(x) for x in data.loc[i, :].values]) for i in data.index])
        columns = 'LocationID", "' + '", "'.join(col for col in desired_cols).replace('.', '_')
        c.execute("""INSERT INTO {} ("{}") VALUES \n("{}")""".format(table_name, columns, values))
        self.conn.commit()
        print('Saved data to table "{}"'.format(table_name))
        pass

    def disconnect_from_database(self):
        self.conn.close()


if __name__ == '__main__':

    config = get_config()
    club_metadata = config[0]
    tables = config[1]
    healthchecks_urls = config[2]

    db = DataBasePreparer(tables)

    for idx in club_metadata.index:

        dh = DataHandler(club_id=idx)

        # wu = dh.data['WeatherUnderground']
        # if ~(hasattr(wu, 'daily') and hasattr(wu, 'hourly') and hasattr(wu, 'text')):
        #     _ping(healthchecks_urls['some_weather_underground_forecast_freqs_missing'])

        for provider in tables.keys():

            dh.conn = connect_to_db(provider)

            for forecast_type in tables[provider].keys():

                try:
                    dh.save_data_to_sql_table(input_data=dh.data[provider],
                                              table_name=forecast_type,
                                              table_columns=tables[provider][forecast_type])
                except Exception as e:
                    print('Exception: {}'.format(e))
                    # raise e

            dh.disconnect_from_database()

        print('\nSaved all data for id {}: {}'.format(idx, club_metadata.loc[idx, 'ClubName']))

    _ping(healthchecks_urls['save_api_data'])
    print('\n\n\nFinished.')
