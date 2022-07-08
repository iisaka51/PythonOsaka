from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

v1 = ws.acell('D1').value
v2 = ws.acell('D1', value_render_option='FORMULA').value
