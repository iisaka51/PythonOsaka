from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

formula = '=GoogleFinance("currency:USDJPY", "average")'
_ = ws.update('B14', formula, raw=False)

v1 = ws.acell('B14').value
