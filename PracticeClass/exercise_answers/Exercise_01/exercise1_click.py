import csv
from is_binary import is_binary

__VERSION__ = "0.1.0"

def readcsv(csvfiles):
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
    import click
    @click.command()
    @click.argument('filepath', type=click.Path(exists=True),
                    required=True, nargs=-1)
    @click.version_option(version=__VERSION__)
    def cli(filepath):
        readcsv(filepath)

    cli()
