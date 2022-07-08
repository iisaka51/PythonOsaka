from openpyxl import Workbook

wb = Workbook()
ws = wb.active

ws.append(['This is A1', 'This is B1', 'This is C1'])
ws.append({'A' : 'This is A1', 'C' : 'This is C1'})
ws.append({1 : 'This is A1', 3 : 'This is C1'})

values = ws.iter_rows(min_row=1, values_only=True)
for val in values:
    print(val)
