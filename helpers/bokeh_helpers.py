from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.ranges import Range1d
from bokeh.layouts import gridplot, widgetbox, column
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Select
import pandas as pd
import datetime as dt
import sqlite3

from utils.read_config import get_locations

locations = get_locations()


def get_data_for_location_id_in_table(location_id, table_name):
    con = sqlite3.connect('DarkSky.db')
    query = "SELECT * FROM {} WHERE locationId = '{}'".format(table_name, location_id)
    df = pd.read_sql_query(query, con)
    values = [pd.to_numeric(df[col], errors='ignore') for col in df.columns]
    df = pd.DataFrame(data=values, index=df.columns).T
    time_cols = [col for col in df.columns if col.lower().endswith('time')]
    for col in time_cols:
        df[col] = df[col].apply(lambda x: dt.datetime.utcfromtimestamp(int(x)))
    df = df.fillna('')
    return df


def get_plot(source, plot_width=800, plot_height=200, x_range=None):
    plot = figure(
        plot_width=plot_width,
        plot_height=plot_height,
        toolbar_location=None,
        tools="pan,box_select,hover,wheel_zoom,box_zoom,tap,reset",
        active_scroll="wheel_zoom",
        x_axis_type='datetime'
    )
    x_col_name = 'time'
    y_col_name = 'active'

    xs = source.data[x_col_name]
    ys = source.data[y_col_name]
    plot.circle(
        source=source,
        x=x_col_name,
        y=y_col_name
    )

    plot.min_border = 30
    if x_range:
        plot.x_range = x_range
    else:
        plot.x_range = Range1d(start=min(xs) - 1, end=max(xs) + 1)
    try:
        plot.y_range = Range1d(start=min(ys) - 1, end=max(ys) + 1)
    except TypeError:
        pass

    return gridplot(
        [[plot]],
        toolbar_options=dict(logo='grey')
    )


def get_dashboard(location_id, table_name):
    df = get_data_for_location_id_in_table(location_id, table_name)
    source = ColumnDataSource(df)
    source.data['active'] = df.iloc[:, 0].values

    print(df.columns)
    plot = get_plot(
        source=source,
    )

    dropdown = Select(
        title='Field',
        value=df.columns[0],
        options=list(df.columns)
    )

    def callback(attr, old, new):
        source.data['active'] = source.data[new]

    dropdown.on_change('value', callback)

    print(plot)
    return (
        gridplot([[column(widgetbox(dropdown), plot)]], merge_tools=True, toolbar_options=dict(logo='grey')),
        df
    )


def get_location_map():
    plot = figure(
        toolbar_location=None,
        tools="pan,box_select,hover,wheel_zoom,box_zoom,tap,reset",
        active_scroll="wheel_zoom"
    )
    plot.circle(0, 0)
    return gridplot(
        [[plot]],
        toolbar_options=dict(logo='grey')
    )
