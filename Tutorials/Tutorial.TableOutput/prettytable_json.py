from prettytable import from_json

with open('CITY.json') as fp:
    json_data = fp.read()

table = from_json(json_data)
print(table)
