import gspread_dataframe as gd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

formula = (
    '=GOOGLEFINANCE("GOOGL","price"'
    ',DATE(2020,2,24),DATE(2020,2,29))'
    )
_ = ws.update('B1', formula, raw=False)

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
max_rows = len(all_rows)

df = gd.get_as_dataframe(ws,
              dtype={0: str, 1:float},
              nrows=max_rows, usecols=[1,2],
              parse_dates=['Date'],
              evaluate_formulas=True)
