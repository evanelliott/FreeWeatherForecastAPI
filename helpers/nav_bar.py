from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def mynavbar():
    return Navbar(
       'Dashboard',
       View('Home', 'weather.index'),
       View('Dashboard', 'weather.forecast')
    )
