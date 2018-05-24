from utils.pipeline import DataBasePreparer, DataHandler
from utils.read_config import get_forecast_metadata, get_credentials
from utils.health_checks import ping

db = DataBasePreparer(tables_metadata_dict=get_forecast_metadata())

dh = DataHandler()
dh.save_forecasts_for_all_locations()
dh.export_data(to_csv=True, to_google_sheets=True)

credentials = get_credentials()
ping(credentials['health_checks_url'])

