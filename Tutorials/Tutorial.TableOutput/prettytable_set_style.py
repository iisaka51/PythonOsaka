from prettytable import PrettyTable,  MARKDOWN, PLAIN_COLUMNS, DEFAULT
from data import data

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

print('DEFAULT style ---------')
table.set_style(DEFAULT)
print(table)

print('\nMARKDOWN style ---------')
table.set_style(MARKDOWN)
print(table)

print('\nPLAIN_COLUMNS style ---------')
table.set_style(PLAIN_COLUMNS)
print(table)

