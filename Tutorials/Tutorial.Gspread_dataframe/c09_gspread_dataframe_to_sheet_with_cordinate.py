import pandas as pd
from gspread_utils import GSpread

ws = GSpread('PythonOsaka_tempfile').worksheet

_ = ws.clear()

df = pd.read_csv('GAFAM.csv')
_ = ws.update( 'B2',
        [df.columns.values.tolist()] + df.values.tolist())
