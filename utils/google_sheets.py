import gspread
import datetime as dt
from oauth2client.service_account import ServiceAccountCredentials


def update_google_sheets_file(file_id, keyfile_path, forecast, index_col_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path, scope)
    gc = gspread.authorize(credentials)

    sh = gc.open_by_key(file_id)
    print('Connected to Google Sheet: {}'.format(file_id))
    print(sh.worksheets())

    for idx, key in enumerate(['observation', 'minutely', 'hourly', 'daily']):
        sheet = sh.get_worksheet(idx)
        sheet.clear()
        print('Cleared all values from Google Sheet {} {}.'.format(idx, key))

        input_df = getattr(forecast, key)
        input_df.index = input_df[index_col_name].apply(
            lambda x: dt.datetime.fromtimestamp(int(float(x))).strftime('%H:%M %a %d/%m'))
        input_df['datetime'] = input_df[index_col_name].apply(lambda x: dt.datetime.fromtimestamp(int(float(x))))

        input_df['index'] = input_df.index.values

        lst = input_df.values.flatten().tolist()

        n_rows = len(input_df.index)
        n_cols = len(input_df.columns)

        cell_list = sheet.range(1, 1, n_rows, n_cols)
        for i in range(len(cell_list)):
            cell = cell_list[i]
            cell.value = str(lst[i])
        sheet.update_cells(cell_list)

        sheet.insert_row(input_df.columns.values.tolist())
        sheet.insert_row(input_df.columns.values.tolist())
        sheet.delete_row(1)

        print('Uploaded df with {} rows and {} columns to Google Sheet {} {}'.format(n_rows, n_cols, idx, key))
