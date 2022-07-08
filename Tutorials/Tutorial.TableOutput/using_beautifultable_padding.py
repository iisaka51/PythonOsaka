import numpy as np
from beautifultable import BeautifulTable

teams_list = ["Dallas", "Chicago", "Los Angeles"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

table = BeautifulTable()
table.columns.header = teams_list
for r in range(len(data)):
    table.rows.append(data[r])

table.columns.padding_left['Dallas'] = 3
table.columns.padding_left['Chicago'] = 5
table.columns.padding_right['Los Angeles'] = 7
print(table)
