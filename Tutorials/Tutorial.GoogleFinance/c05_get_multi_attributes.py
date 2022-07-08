import pandas as pd
import gspread_dataframe as gd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

df = pd.read_csv('GAFAM.csv', index_col=0)

df2 = df.T

attributes = ["price", "high", "low", "volume", "volumeavg", "pe", "eps" ]
for y in attributes:
    row = [f'=GoogleFinance("{x}", "{y}")'  for x in df2.loc['Ticker']]
    df2.loc[y] = row

start_col = 2
_ = gd.set_with_dataframe(ws, df2, include_index=True, row=1, col=start_col)

all_rows = ws.get_all_values()
columns = all_rows.pop(0)
max_rows = len(all_rows)

df3 = gd.get_as_dataframe(ws,
              nrows=max_rows, usecols=[1,2,3,4,5,6],
              index_col=0,
              evaluate_formulas=True)
