"""
sample myconfig.ini

[csvfile]
searchpath: /var/tmp:/tmp

"""

import os, sys
import configparser as config
import csv
from is_binary import is_binary

def get_dirs(configfile):
    parser = config.ConfigParser()
    parser.read(configfile)
    for conf in parser.items('csvfile'):
        if conf[0] == 'searchpath':
            dirpath = set(conf[1].split(':'))
    dirpath.add(os.getcwd())
    return list(dirpath)

def get_filepaths(**kwargs):
    filepaths = list()
    missing = list()
    for file in kwargs['filename']:
        if not os.path.exists(file):
            if os.path.dirname(file) != '':
                missing.append(file)
                continue
            filename = os.path.basename(file)
            for dir in kwargs['dirs']:
                path = os.path.join(dir, filename)
                if os.path.exists(path):
                    filepaths.append(path)
                    break
            else:
                missing.append(file)
        else:
            filepaths.append(file)

    return (filepaths, missing)

def readcsv(filepath):
    print(f'--- {filepath} ----')
    if is_binary(filepath):
        print('This is not CSVfile.')
        return

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
    @click.option('-f', '--configfile', type=click.Path(),
                  default='./myconfig.ini',
                  help='Path to configuration file')
    @click.option('--debug', is_flag=True, help='DEBUG mode')
    @click.argument('filename', type=click.Path(), #exists=False),
                    required=True, nargs=-1)
    def cli(**kwargs):
        kwargs['dirs'] = get_dirs(kwargs['configfile'])
        filepaths, missing = get_filepaths(**kwargs)

        for file in missing:
            print(f'{file}: No such file or directory')

        for csvfile in filepaths:
            readcsv(csvfile)

    cli()

