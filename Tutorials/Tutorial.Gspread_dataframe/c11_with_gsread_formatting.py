import pandas as pd
from gspread_utils import GSpread
import gspread_dataframe as gd
from gspread_formatting.dataframe import format_with_dataframe

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

df = pd.read_csv('GAFAM.csv')
gd.set_with_dataframe(ws, df)
_ = format_with_dataframe(ws, df, include_column_header=True)
