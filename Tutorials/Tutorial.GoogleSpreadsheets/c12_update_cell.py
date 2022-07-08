from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

prev_d1 =  ws.acell('D1').value
cell_c1 =  ws.update_cell(1,3, 120)
cell_d1 =  ws.acell('D1').value

# prev_d1
# cell_c1
# cell_d1
