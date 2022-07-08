from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

formula = '=ArrayFormula(IF(B1:B12>60, "Upper", "Lower"))'
_ = ws.update('E1', formula, raw=False)
