from prettytable import from_csv

with open("CITY.csv") as fp:
    table = from_csv(fp)

print(table)
