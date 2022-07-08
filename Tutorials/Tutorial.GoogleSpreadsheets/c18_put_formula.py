from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

_ = ws.update('B13', '=AVERAGE(B1:B12)', raw=False)
_ = ws.update('C13', '=AVERAGE(C1:C12)')

v1 = ws.acell('B13').value
v2 = ws.acell('B13', value_render_option='FORMULA').value
v3 = ws.acell('C13').value
v4 = ws.acell('C13', value_render_option='FORMULA').value
