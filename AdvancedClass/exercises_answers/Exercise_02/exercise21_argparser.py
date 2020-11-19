import csv

def readcsv(filepath):
        print(f'--- {filepath} ----')
        with open(filepath) as f:
            data = csv.reader(f)
            for row in data:
                print(row)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description ='show CSV files')
    parser.add_argument(dest ='filepath', metavar ='filepath', nargs ='*')
    args = parser.parse_args()
    for filepath in args.filepath:
        readcsv(filepath)
