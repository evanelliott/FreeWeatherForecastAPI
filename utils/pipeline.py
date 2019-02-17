import sqlite3
import datetime as dt
import pandas as pd
from api.dark_sky import DarkSkyWeatherForecast
from utils.read_config import get_forecast_metadata, get_credentials, get_locations
from utils.google_sheets import update_google_sheets_file


def connect_to_db(db_name):
    conn = sqlite3.connect('{}.db'.format(db_name))
    print("\nConnected to database '{}'".format(db_name))
    return conn


class DataBasePreparer(object):
    def __init__(self, tables_metadata_dict):
        self.conn = None
        self.tables = tables_metadata_dict
        for db_name in ['DarkSky']:
            self.conn = connect_to_db(db_name)
            for tbl in tables_metadata_dict.keys():
                self.delete_table_if_exists(table_name=tbl)
                self.create_table(table_name=tbl, columns=tables_metadata_dict[tbl])
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
    def __init__(self):
        self.locations = get_locations()
        self.forecast_metadata = get_forecast_metadata()
        self.credentials = get_credentials()
        self.data = None
        self.conn = None
        self.all_data = {}

    def get_forecast(self, location_id):
        print('\n\nGetting data for id {}: {}'.format(location_id, self.locations.loc[location_id, 'PlaceName']))
        lat = self.locations.loc[location_id, 'Latitude']
        lon = self.locations.loc[location_id, 'Longitude']
        self.data = DarkSkyWeatherForecast(latitude=lat, longitude=lon, api_key=self.credentials['dark_sky_api_key'])

    def filter_columns(self, table_name, table_columns, location_id):
        data = getattr(self.data, table_name)
        desired_cols = [col for col in table_columns if col in data.columns]
        data = data.loc[:, desired_cols]
        data.loc[:, 'LocationID'] = location_id
        setattr(self.data, table_name, data)

    def save_data_to_sql_table(self, data, table_name):
        c = self.conn.cursor()
        data = getattr(data, table_name)
        values = '"),\n("'.join(
            ['", "'.join([str(x) for x in data.loc[i, :].values]) for i in data.index])
        columns = '", "'.join(col for col in data.columns).replace('.', '_')
        c.execute("""INSERT INTO {} ("{}") VALUES \n("{}")""".format(table_name, columns, values))
        self.conn.commit()
        print('Saved data to table "{}"'.format(table_name))
        pass

    def save_forecasts_for_all_locations(self):
        for location in self.locations.index:
            self.get_forecast(location_id=location)
            self.conn = connect_to_db('DarkSky')
            for key in self.forecast_metadata.keys():
                table_name = key
                table_columns = self.forecast_metadata[key]
                self.filter_columns(table_name=table_name, table_columns=table_columns, location_id=location)
                try:
                    self.save_data_to_sql_table(data=self.data, table_name=key)
                except Exception as e:
                    print('Exception: {}'.format(e))
            self.disconnect_from_database()

    def save_csv_files(self, index_col_name):
        for key in ['observation', 'minutely', 'hourly', 'daily']:
            data = getattr(self.all_data, key)
            data.index = data[index_col_name].apply(
                lambda x: dt.datetime.fromtimestamp(int(float(x))).strftime('%H:%M %a %d/%m'))
            data['datetime'] = data[index_col_name].apply(lambda x: dt.datetime.fromtimestamp(int(float(x))))

            data.to_csv('DarkSky_{}.csv'.format(key))

    def export_data(self, to_csv=True, to_google_sheets=False):
        self.load_data_from_sqlite()
        if to_csv:
            self.save_csv_files(index_col_name='time')
        if to_google_sheets:
            update_google_sheets_file(file_id=self.credentials['google_sheets_file_id'],
                                      keyfile_path=self.credentials['google_sheets_keyfile_path'],
                                      all_data=self.all_data, index_col_name='time')

    def load_data_from_sqlite(self):
        conn = sqlite3.connect('DarkSky.db')
        for key in ['observation', 'minutely', 'hourly', 'daily']:
            df = pd.read_sql_query("SELECT * FROM {}".format(key), conn)
            self.all_data[key] = df
        print('\n\nLoaded all data from sqlite.')

    def disconnect_from_database(self):
        self.conn.close()
