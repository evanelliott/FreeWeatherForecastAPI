from flask import Blueprint, render_template, request, make_response, abort
from jinja2 import TemplateNotFound
from bokeh.embed import components
from helpers import bokeh_helpers
import sqlite3
import pandas as pd
import datetime as dt

blueprint = Blueprint(
    name='weather',
    import_name=__name__,
    template_folder='templates'
)


@blueprint.route('/')
def index():
    try:
        map = bokeh_helpers.get_location_map()
        script, div = components(map)
        template_data = {
            'time': dt.datetime.now(),
            'div': div,
            'script': script,
        }
        return render_template(
            template_name_or_list='index.html',
            **template_data
        )
    except TemplateNotFound:
        abort(404)


@blueprint.route('/forecast')
def forecast():
    try:
        location_id = request.args['location_id']
        table_name = request.args['table']
        (plot, df) = bokeh_helpers.get_dashboard(location_id, table_name)
        script, div = components(plot)

        print(script)
        print(div)
        print(df)
        template = render_template(
            template_name_or_list='forecast.html',
            script=script,
            div=div,
            df=df.to_html(),
        )
        return template
    except TemplateNotFound as e:
        print(e)
        abort(404)
