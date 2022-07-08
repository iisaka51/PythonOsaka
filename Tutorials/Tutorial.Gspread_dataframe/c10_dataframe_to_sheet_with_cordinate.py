import pandas as pd
from gspread_utils import GSpread
import gspread_dataframe as gd

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

df = pd.read_csv('GAFAM.csv')
gd.set_with_dataframe(ws, df, row=2, col=2)
