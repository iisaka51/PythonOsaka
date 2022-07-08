from gspread_utils import GSpread

gs = GSpread("PythonOsaka_GSpread_Tutorial")

v1 = gs.workbook.sheet1
v2 = gs.workbook.worksheets()
v3 = gs.workbook.worksheet("シート2")

gs = GSpread("PythonOsaka_GSpread_Tutorial", "シート2")
v4 = gs.worksheet
