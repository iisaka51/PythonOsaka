import re
from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

regexp = re.compile(r'2022/.*/01')
cell_list = ws.findall(regexp)

