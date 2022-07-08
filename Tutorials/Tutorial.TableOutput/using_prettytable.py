import numpy as np
from prettytable import PrettyTable

teams_list = ["Dallas", "Chicago", "Los Angeles"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

table = PrettyTable(field_names = teams_list)
for row in data:
    table.add_row(row)

print(table)

