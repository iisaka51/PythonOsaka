import pandas as pd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet

all_rows = ws.get_all_values()
df = pd.DataFrame(all_rows, columns=[0,1,2,3])

df[[0]] = df[[0]].apply(pd.to_datetime)
df[[1,2,3]] = df[[1,2,3]].apply(pd.to_numeric)

# df
# df.dtypes
