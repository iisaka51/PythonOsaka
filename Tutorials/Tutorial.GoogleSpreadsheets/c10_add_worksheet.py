from gspread_utils import GSpread

gs = GSpread("PythonOsaka_GSpread_Tutorial", "シート2")

ws1 = gs.workbook.duplicate_sheet(gs.worksheet.id,
             insert_sheet_index=2, new_sheet_name='Sheet3')
ws2 = gs.workbook.add_worksheet(title="Finance", rows="10", cols="10")
# _ = gs.workbook.del_worksheet(ws1)
# _ = gs.workbook.del_worksheet(ws2)
