from pycel import ExcelCompiler

# See Also: c22_openpyxl_addd_formula.py

excel = ExcelCompiler('output_formula.xlsx')

val1 = excel.evaluate('Sheet!A1')
val2 = excel.evaluate('Sheet!A2')

excel.set_value('Sheet!A1', 100)
val3 = excel.evaluate('Sheet!A1')
val4 = excel.evaluate('Sheet!A2')

# val1
# val2
# val3
# val4
