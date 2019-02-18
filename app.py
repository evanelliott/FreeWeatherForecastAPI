from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from helpers.nav_bar import nav
from blueprints.weather import blueprint

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    nav.init_app(app)
    Bootstrap(app)
    app.run(port=5002, debug=True)
