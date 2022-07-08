from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

prev_data = ws.get_all_values()

cell_list = ws.range('E1:E12')
for cell in cell_list:
    cell.value = 300

_ = ws.update_cells(cell_list)

data = ws.get_all_values()

# prev_data
# data
