import csv
from is_binary import is_binary

__VERSION__ = "0.1.0"

def cmd(csvfiles):
    for filepath in csvfiles:
        print(f'--- {filepath} ----')
        if is_binary(filepath):
            print('This is not CSVfile.')
            continue
        with open(filepath) as f:
            data = csv.reader(f)
            rawcount = 0
            for row in data:
                print(row)
                rawcount += 1
            else:
                if rawcount == 0:
                    print('This is empty CSVFile.')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description ='show CSV files')
    parser.add_argument(dest ='filepath', metavar ='filepath', nargs ='*')
    args = parser.parse_args()
    cmd(args.filepath)
