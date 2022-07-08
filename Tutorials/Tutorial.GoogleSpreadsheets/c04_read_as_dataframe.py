import pandas as pd
from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
df = pd.DataFrame(all_rows, columns=columns)

new_columns = list(df.columns.values.tolist())
values = df.values.tolist()

# to Google Spreadsheets
# ws.update(new_columns + values)
