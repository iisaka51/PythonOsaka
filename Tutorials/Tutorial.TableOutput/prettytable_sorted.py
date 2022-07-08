from prettytable import PrettyTable
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

table.sortby = 'Area'
print(table)

table.sortby = 'Population'
print(table.get_string(title='Reverse', reversesort=True))

