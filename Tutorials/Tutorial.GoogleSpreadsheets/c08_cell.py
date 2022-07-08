from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

data =  ws.cell(3,1).value

# data
