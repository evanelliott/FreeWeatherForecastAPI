# FreeWeatherForecastAPI

This is a test repo for getting free weather forecast data from the DarkSky API.

- takes as input a config csv containing desired lat/lon coordinates
- accesses API with python urllib.requests
- saves daily, hourly, and minutely weather forecasts to local sqlite database
- other scripts to export forecasts to csv or google sheets

### What does it do?
- Gets DarkSky weather forecast data for locations of your choice.
- Automatically saves to local database.
- Can save to csv and/or Google Sheets if desired.

### How does it do it?
- HTTP requests to DarkSky RESTful API
- Decodes JSON response via pd.io.json.json_normalize()
- SQLite & pyodbc database tools built-in to Python as standard
- (Optional) pd.to_csv(); gspread ****************LINK************** to interface with Google Sheets API

### How do I use it?
- Setting up environment
code install requirements.txt
```
$ pip install -r requirements.txt --no-index --find-links file:///tmp/packages
```
- Getting credentials from DarkSky
link to DarkSky; mention daily call-limit; forecast products; forecast features; geographical domain boundaries;
- Specifying forecast locations
explain how to modify config.locations.csv
- Setting up a database (and getting SQLiteStudio) as default
- Setting up Google Sheets (and getting credentials)
- Single use versus task scheduling
- Monitoring continuous deployment with HealthChecks

#### Powered by DarkSky
