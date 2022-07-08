import csv

with open('sample.csv') as f:
    data = csv.reader(f)
    for row in data:
        print(row)
