from prettytable import PrettyTable
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

print(table)

table.clear_rows()
print(table)
