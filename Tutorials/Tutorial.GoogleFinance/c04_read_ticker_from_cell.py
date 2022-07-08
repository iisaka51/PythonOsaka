import pandas as pd
import gspread_dataframe as gd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

df = pd.read_csv('GAFAM.csv')

start_col = 2
max_row = len(df)
formula = [ f'=GoogleFinance(C{x + start_col},"price")'
                    for x in range(max_row)]
df['Price'] = formula

_ = gd.set_with_dataframe(ws, df, row=1, col=start_col)

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
max_rows = len(all_rows)

df = gd.get_as_dataframe(ws,
              dtype={0: str, 1: str, 2:float},
              nrows=max_rows, usecols=[1,2,3],
              evaluate_formulas=True)
