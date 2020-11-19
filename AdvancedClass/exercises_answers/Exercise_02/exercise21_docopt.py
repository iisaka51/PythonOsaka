import csv

__VERSION__='1.0'

__doc__="""show CSV files
Usage: {prog} [-h|--help]
       {prog} <filepath>...

Arguments:
  FILEPATH        path to CSVfile

Options:
  -h, --help                   show this help message and exit
""".format(prog=__file__)

def readcsv(csvfiles):
        print(f'--- {filepath} ----')
        with open(filepath) as f:
            data = csv.reader(f)
            for row in data:
                print(row)

if __name__ == '__main__':
    import sys
    from docopt import docopt

    args = docopt(__doc__,version=__VERSION__)
    if len(args['<filepath>']) == 0:
        sys.argv.append('--help')
        args = docopt(__doc__,version=__VERSION__)

    for filepath in args['<filepath>']:
        readcsv(filepath)
