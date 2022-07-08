from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

cell = ws.find("2022/02/01")

v1 = f"Found at Row:{cell.row} Col:{cell.col}"
