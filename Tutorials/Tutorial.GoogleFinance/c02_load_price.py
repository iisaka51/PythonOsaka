import gspread_dataframe as gd
from gspread_utils import GSpread
from c02_get_symbols import read_ticker

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

df = read_ticker('GAFAM.csv')
gd.set_with_dataframe(ws, df)
