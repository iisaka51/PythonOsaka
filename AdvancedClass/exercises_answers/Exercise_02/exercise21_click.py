import csv

def readcsv(filepath):
    print(f'--- {filepath} ----')
    with open(filepath) as f:
        data = csv.reader(f)
        for row in data:
            print(row)

if __name__ == '__main__':
    import click
    @click.command()
    @click.argument('filepath', type=click.Path(exists=True),
                    required=True, nargs=-1)
    def cli(**kwargs):
        for filepath in kwargs['filepath']:
            readcsv(filepath)

    cli()
