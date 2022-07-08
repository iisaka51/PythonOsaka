import numpy as np
from rich.console import Console
from rich.table import Table

teams_list = ["Dallas", "Chicago", "Los Angelos"]
data = np.array([[1, 2, 1],
                 [0, 1, 0],
                 [2, 4, 1]])

table = Table()
for team in teams_list:
    table.add_column(team)

for i in range(len(data)):
   row_data = ""
   for j in range(len(data[i])):
        row_data += str(j)
   table.add_row(row_data)

console = Console()
console.print(table)
