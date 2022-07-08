from prettytable import PrettyTable
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

table.header = False
table.border = False
table.padding_width = 6
print(table)
