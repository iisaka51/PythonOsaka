import xlwings as xw

wb = xw.Book('output_formula.xlsx')
ws = wb.sheets.active
# ws = wb.sheets['Sheet']
# ws = wb.sheets[0]

val1 = ws.range('A1').value
val2 = ws.range('A2').value

val3 = ws.range('A1').value = 100
val4 = ws.range('A2').value

# val1
# val2
# val3
# val4
