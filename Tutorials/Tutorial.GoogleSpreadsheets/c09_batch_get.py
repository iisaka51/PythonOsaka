from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

all_rows = ws.get_all_values()
data =  ws.batch_get(['A1:A12', 'D1:D12'])

# data
