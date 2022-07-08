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

new_table = table.rows[:2]
print(new_table)

new_table = table.columns[:2]
print(new_table)
