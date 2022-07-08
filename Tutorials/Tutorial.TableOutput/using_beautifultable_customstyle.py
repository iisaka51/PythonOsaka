import numpy as np
from beautifultable import BeautifulTable


teams_list = ["Dallas", "Chicago", "Los Angelos"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

table = BeautifulTable()
table.columns.header = teams_list
for r in range(len(data)):
    table.rows.append(data[r])

table.set_style(BeautifulTable.STYLE_NONE)  # clear all formatting
table.border.left = 'o'
table.border.right = 'o'
table.border.top = '<~>'
table.border.bottom = '='
table.columns.header.separator = '^'
table.columns.separator = ':'
table.rows.separator = '~'

print(table)
