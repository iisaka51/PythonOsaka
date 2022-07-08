import numpy as np
from beautifultable import BeautifulTable
from termcolor import colored

teams_list = ["Dallas", "Chicago", "Los Angeles"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

table = BeautifulTable()
table.columns.header = teams_list
for r in range(len(data)):
    table.rows.append(data[r])

table.rows.append([
    colored("Dallas", "blue"),
    colored("Chicago", "cyan"),
    colored("Los Angeles", "red")
    ])

print(table)
