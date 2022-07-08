from prettytable import PrettyTable
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

print(table.get_string(fields=['City name', 'Area']))
print(table.get_string(start=2, end=5))
print(table.get_string(start=2, end=5, fields=['City name', 'Population']))
