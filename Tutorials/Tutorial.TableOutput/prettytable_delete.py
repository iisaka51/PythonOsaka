from prettytable import PrettyTable
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

print(table)

table.del_row(0)
table.del_column("Annual Rainfall")
print(table)
