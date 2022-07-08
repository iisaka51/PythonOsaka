import csv
from is_binary import is_binary
from prompt_toolkit.shortcuts import message_dialog

def readcsv(csvfiles):
    for filepath in csvfiles:
        print(f'--- {filepath} ----')
        if is_binary(filepath):
            print('This is not CSVfile.')
            continue
        text = str()
        with open(filepath) as f:
            data = csv.reader(f)
            rawcount = 0
            for row in data:
                print(''.join(row))
                text += ''.join(row) + '\n'
                rawcount += 1
            else:
                if rawcount == 0:
                    print('This is empty CSVFile.')
        message_dialog( title=filepath, text=text).run()

if __name__ == '__main__':
    import click
    @click.command()
    @click.argument('filepath', type=click.Path(exists=True),
                    required=True, nargs=-1)
    def cli(filepath):
        readcsv(filepath)

    cli()
