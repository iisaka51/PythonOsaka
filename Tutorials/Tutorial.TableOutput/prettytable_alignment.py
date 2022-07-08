from prettytable import PrettyTable
from data import data`

table = PrettyTable()
for key, val in data.items():
    table.add_column(key, val)

table.align["City name"] = "l"
table.align["Population"] = "c"
table.align["Annual Rainfall"] = "r"

print(table)
