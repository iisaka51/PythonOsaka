from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

v1 = ws.row_values(1)
v2 = ws.col_values(1)

# v1
# v2
