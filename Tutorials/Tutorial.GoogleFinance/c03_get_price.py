import gspread_dataframe as gd
from gspread_utils import GSpread

ws = gs = GSpread('PythonOsaka_tempfile').worksheet

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
max_rows = len(all_rows)
df = gd.get_as_dataframe(ws,
              dtype={0: str, 1:str, 2:float},
              evaluate_formulas=True,
              nrows=max_rows, usecols=columns)

