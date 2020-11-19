import csv

data = [['A1','B1','C1'],
        ['A2','B2','C2'],
        ['A3','B3','C3']]

with open('sample.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)
