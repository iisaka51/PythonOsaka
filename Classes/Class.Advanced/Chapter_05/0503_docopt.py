from docopt import docopt

__VERSION__='1.0'

__doc__="""Search some files
Usage: {prog} [-v] [--version] [-h|--help]
       {prog} [-p <PATTERN>] [-o <OUTFILE>] [--overwrite] <FILE>...
       {prog} [--pat=<PATTERN>][--outfile=<OUTFILE>] [--overwrite] <FILE>...

Arguments:
  FILE        target file

Options:
  -h, --help                   show this help message and exit
  --version                    show version
  -v, --verbose                verbose mode
  -o OUTFILE, --outfile=OUTFILE output file
  -p PATTER, --pat=PATTERN     search pattern
  --overwrite                  overwrite if file existing
""".format(prog=__file__)

args = docopt(__doc__,version=__VERSION__)
print(args)
