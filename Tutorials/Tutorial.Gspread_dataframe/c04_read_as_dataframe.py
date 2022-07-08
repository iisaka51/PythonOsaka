import gspread_dataframe as gd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_GSpread_Tutorial', "シート2").worksheet

df1 = gd.get_as_dataframe(ws,
              dtype={0: str, 1:int, 2:int, 3:str},
              parse_dates=[0], header=None, evaluate_formulas=True,
              nrows=12, usecols=[0,1,2,3])

df2 = gd.get_as_dataframe(ws,
              dtype={0: str, 1:int, 2:int, 3:str},
              parse_dates=[0], header=None,
              nrows=12, usecols=[0,1,2,3])

v1 = f'{type(df1[0][0])}, {type(df1[1][0])}'
v2 = f'{type(df2[0][0])}, {type(df2[1][0])}'
