from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

v1 = ws.acell('A3').value
v2 = ws.acell('A3:A4').value
v3 = ws.get_values('A3')
v4 = ws.get_values('A3:A4')
v5 = ws.range('A3:A4')
v6 = [c.value for c in v5]
