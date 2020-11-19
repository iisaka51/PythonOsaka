import sys
import csv

def main(filename):
    with open(sys.argv[1]) as f:
        for row in csv.reader(f):
            data = ''.join(row)

main(sys.argv[1])
