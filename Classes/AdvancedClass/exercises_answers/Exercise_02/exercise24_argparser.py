"""
sample myconfig.ini

[csvfile]
searchpath: /var/tmp:/tmp

"""

import os, sys
import configparser as config
import argparse
import csv
from is_binary import is_binary

def get_dirs(agrs):
    parser = config.ConfigParser()
    parser.read(args.configfile)
    for conf in parser.items('csvfile'):
        if conf[0] == 'searchpath':
            dirpath = set(conf[1].split(':'))
    dirpath.add(os.getcwd())
    return list(dirpath)

def get_filepaths(args):
    filepaths = list()
    missing = list()
    for file in args.filename:
        if not os.path.exists(file):
            if os.path.dirname(file) != '':
                missing.append(file)
                continue
            filename = os.path.basename(file)
            for dir in args.dirs:
                path = os.path.join(dir, filename)
                if os.path.exists(path):
                    filepaths.append(path)
                    break
            else:
                missing.append(file)
        else:
            filepaths.append(file)

    return (filepaths, missing)

def cmd(args):
    for filepath in args.filepaths:
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

parser = argparse.ArgumentParser(description = 'show CSV files')
parser.add_argument(dest = 'filename', metavar = 'filename',
                    nargs='+', help ='path to csvfiles')
parser.add_argument('-f', '--configfile', metavar ='filepath',
                    dest='configfile', default='myconfig.ini',
                    help='path to configfile')
parser.add_argument('--debug',
                    dest='debug', action='store_true', default=False,
                    help=argparse.SUPPRESS)

args = parser.parse_args()
args.dirs = get_dirs(args)
args.filepaths, args.missing = get_filepaths(args)

if args.debug:
    print(args)

for file in args.missing:
    print(f'{file}: No such file or directory')

cmd(args)
