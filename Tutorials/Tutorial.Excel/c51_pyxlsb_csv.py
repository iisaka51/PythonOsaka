import csv
from pyxlsb import open_workbook

with open_workbook('test.xlsb') as wb:
    for name in wb.sheets:
        with wb.get_sheet(name) as sheet, open(name + '.csv', 'w') as f:
            writer = csv.writer(f)
            for num, row in enumerate(sheet.rows()):
                if num <= 10:
                    wc = writer.writerow([c.v for c in row])
