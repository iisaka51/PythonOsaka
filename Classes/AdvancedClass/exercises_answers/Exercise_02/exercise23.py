import os
import sys
import csv
from is_binary import is_binary

def readcsv(filepath):
    print(f'--- {filepath} ----')
    if is_binary(filepath):
        print("This is not CSVfile.")
        return

    with open(filepath) as f:
        data = csv.reader(f)
        for row in data:
            print(row)
        else:
            print("This is empty CSVfile")


if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        try:
            readcsv(filepath)
        except FileNotFoundError:
            print(f"{filepath}: No such file or directory.")
    else:
        progname = os.path.basename(sys.argv[0])
        print(f"\n\tUsage: {progname} <CSVfile> [CSVfile...]\n")
