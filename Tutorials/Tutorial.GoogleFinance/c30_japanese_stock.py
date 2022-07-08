from gspread_utils import GSpread

_TICKER="7203:TYO"

ws = GSpread('PythonOsaka_tempfile').worksheet
_ = ws.clear()

formula = (
    f'=IMPORTXML("https://www.google.com/finance/quote/{_TICKER}",'
     '"//*[@class=\'YMlKec fxKbKc\']")'
    )

_ = ws.update('B1', formula, raw=False)

v1 = ws.acell('B1').value
