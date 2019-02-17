# FreeWeatherForecastAPI

Build the Backend of your very own weather forecast app in under 30 minutes with Python.

***

## What does it do?
This code gets free weather forecast data for locations of your choice. [DarkSky][1] provide the data for any location worldwide based on a pair of latitude and longitude coordinates. According to the DarkSky [Terms of Service](https://darksky.net/dev/docs/terms) users are granted full permission to use the data for commercial purposes, as long as the message “Powered by Dark Sky” is legibly displayed somewhere near the data. Users are allowed to make up to 1,000 free calls per day to the API, so that is a lot of free data! :smiley:

The code downloads the weather forecast data into a single local database. Within the database, separate tables are created for the current weather observations, daily forecasts, hourly forecasts, and minutely forecasts. This effectively takes a “snapshot” of the data which means an app can be served without having to make successive calls to the API each time a page is loaded.

Optionally, weather forecasts can be exported in alternative formats to share data more easily. One option is to export as CSV for Excel users, or alternatively you can write to Google Sheets but bear in mind you will need to set up credentials to do the latter.

***

## How does it do it? 
The code is intended to perform as a simple “black box” for users. That being said, developers may find it useful to have a high-level description of its working parts. It is also a good opportunity to showcase some really nice Python tools.

The code sends HTTP requests to the [DarkSky RESTful API][1] via Python’s [urllib][3] module. The “get” request contains important information, that is the latitude and longitude coordinates of the forecast location and your API key which can be obtained [here][1]. The old favourite [Pandas][4] plays a key role in translating the data. Its [json_normalize()](https://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.io.json.json_normalize.html) method is a very convenient way of decoding the standard API response from a ([JSON](https://www.json.org/)) nested set of sets and putting it in a nice familiar [DataFrame](http://pandas.pydata.org/pandas-docs/version/0.21/generated/pandas.DataFrame.html) object. This part of the code is encapsulated in the *DarkSkyWeatherForecast* object. The current observation; daily, hourly, and minutely forecasts exist as attributes of the overall class. I personally find it useful to envisage this class as a little parcel of data, falling out of the API into the pipeline on its way to be delivered to the database. :smiley:

The database engineering is handled by a small number of Python modules. [SQLite][5] creates a lightweight disk-based relational database in your working directory where all the data is stored. [PyODBC][6] is a module that makes it easy to access ODBC databases. Together these modules do the “heavy lifting” of the data pipeline. [Gspread][7] is a neat little library which does the task of exporting your data to Google Sheets. It uses the deprecated [oauth2client][8] module to authenticate your access securely to the [Google Sheets API][2].

***

## How do I use it?
### •	Setting up environment
Run this command…
```
$ pip install -r requirements.txt --no-index --find-links file:///tmp/packages
```

### •	Getting credentials from DarkSky
Link to the [website][1]

### •	Specifying forecast locations
The locations are kept in the *config -> locations.csv* file. By default the capital cities of Great Britain are provided as an example.

### •	Setting up a database
The database is created automatically by the code. If you want a more intuitive interaction with the database I would recommend downloading [SQLiteStudio](https://sqlitestudio.pl/index.rvt). Its user interface (UI) makes it easy to query the data and generally observe the data in its natural habitat. :smiley:

### • Preparing Google Sheets
This option will add about 10 minutes on to the setup time. Essentially you need two pieces of data for this to work. The first is a free *“service account key”* file which will allow you to log in to the Google Sheets Developers API. [This page](http://gspread.readthedocs.io/en/latest/oauth2.html) explains how to get your service account key file. The second is a *“keyfile id”* which relates to the id of your destination document in the Google cloud. Importantly, your Google Sheets file must contain four sheets named "observation", "minutely", "hourly", and "daily" in order for the code to find them. Next you will need to copy/paste the service account key filepath and your keyfile id into the *config -> credentials.ini* file.

### •	Executing the script
The script *main.py* downloads the latest forecasts for the locations you have configured. The *DataBasePreparer* will initially clear any pre-existing data, and then it will prepare the database tables according to the set of columns provided in *config -> forecast_metadata.ini*. It will then cycle through the locations and append their forecasts to the relevant tables. Finally it will export the data to CSV and/or Google Sheets depending on the key-word arguments (kwargs) passed to the *DataHandler.export_data()* method.

### •	Single use versus task-scheduling
Downloading the latest forecast on an ad-hoc basis can be done by running the main.py script. On the other hand, what if you want to automatically update the forecasts on a daily basis? The answer is scheduling the task and there are many ways you could do this depending on your preferences. I personally find [Jenkins][9] to be a really great option since it is free, deployable on Windows or Linux machines, and provides handy “build logs” containing console output. When writing deployment code, I think it is always a good idea to keep a traceable account of my builds so I can catch bugs as and when they will surely appear. :smiley:

### •	Monitoring continuous deployment
[HealthChecks][10] is a really useful free tool which can monitor your software and alert you if something goes wrong. It is set up to expect a periodic “ping” as often as your task is scheduled to occur, and if it does not receive its signal in the allotted time it will send an email to you. The “pings” can be triggered by the final line of a script to indicate the job has completed successfully.

### •	Bonus Hint….
If connected to Google Sheets, the free dashboard tool [Tableau Public][11] automatically pulls new data each day.

***

## Thanks
I am very grateful for all the open-source software upon which this tiny project is built. Without your collaboration many projects like this would not be possible. In case you missed the links above, here they are again:

[DarkSky][1]
[Google Sheets API][2]
[Urllib][3]
[Pandas][4]
[SQLite][5]
[Pyodbc][6]
[Gspread][7]
[Oauth2client][8]
[Jenkins][9]
[HealthChecks][10]
[Tableau Public][11]

[1]: https://darksky.net/dev
[2]: https://developers.google.com/sheets/api/
[3]: https://docs.python.org/3/library/urllib.html
[4]: https://pandas.pydata.org/
[5]: https://www.sqlite.org/index.html
[6]: http://mkleehammer.github.io/pyodbc/
[7]: https://gspread.readthedocs.io/en/latest/
[8]: https://pypi.org/project/oauth2client/
[9]: https://jenkins.io/
[10]: https://healthchecks.io/
[11]: https://public.tableau.com/en-us/s/

[**<p align="center">Powered by DarkSky</p>**](https://darksky.net/poweredby/)
