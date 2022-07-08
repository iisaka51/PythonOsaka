import xlwings as xw
import pandas as pd

wb = xw.Book('test.xlsx')
ws = wb.sheets.active

df = ws.range('A1:G10').options(pd.DataFrame, header=1).value

# df
# wb.close()
