from prettytable import from_html

with open('CITY2.html') as fp:
    data = fp.read()

tables = from_html(data)
for table in tables:
    print(table)
