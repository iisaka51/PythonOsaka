from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

_ = ws.format('A1:A12', {'textFormat': {'bold': True}})
# _ = ws.format('A1:A12', {'textFormat': {'bold': False}})
