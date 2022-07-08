import numpy as np
from gspread_utils import GSpread

ws = GSpread("PythonOsaka_GSpread_Tutorial", "シート2").worksheet

array = np.array(ws.get_all_values())

array2 = np.array([[1, 2, 3], [4, 5, 6]])
# ws.update('F1', array2.tolist())
