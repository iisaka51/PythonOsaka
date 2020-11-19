import sys
import csv

def readcsv(filepath):
    print(f'--- {filepath} ----')
    with open(filepath) as f:
        data = csv.reader(f)
        for row in data:
            print(row)


if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        readcsv(filepath)
