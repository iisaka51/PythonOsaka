from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

v1 = ws.get_all_values()
v2 = ws.get_all_records()

# v1
# v2
