from gspread_utils import GSpread

_TICKER="7203"

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

formula = f'=TokyoStockPrice({_TICKER})'

_ = ws.update('B2', formula, raw=False)

v1 = ws.acell('B2').value
