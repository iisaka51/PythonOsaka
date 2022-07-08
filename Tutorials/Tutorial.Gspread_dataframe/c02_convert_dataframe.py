import pandas as pd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet

data1 = ws.get_all_values()
df1 = pd.DataFrame(data1, columns=[0,1,2,3])

data2 = ws.get_all_values(value_render_option='FORMULA')
df2 = pd.DataFrame(data2, columns=[0,1,2,3])

v1 = f'{type(df1[0][0])}, {type(df1[1][0])}'
v2 = f'{type(df2[0][0])}, {type(df2[1][0])}'

# df1
# df2
