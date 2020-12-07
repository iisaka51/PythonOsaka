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
    import typer
    from typing import List

    def print_version(version: bool):
        if version:
            typer.echo(f'Version: {__VERSION__}')
            raise typer.Exit()

    def cli(filepath: List[str] = typer.Option([], '--filepath',
                                   metavar='FILE_PATH',
                                   help="Path to CSVFile."),
            version: bool = typer.Option(False, '--version',
                                   callback=print_version,
                                   help="Show version and exit.")
        ):
        readcsv(filepath)

    typer.run(cli)
