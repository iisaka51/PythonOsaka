"""dump database"""

from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface
from .dblogging import log

NAME = 'dump'
PROGRAM = 'dbmanager dump'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
       {PROGRAM} DBNAME
       {PADDING} [--verbose] [--debug]
       {PADDING} [--help]

"""

HELP = f"""\
{USAGE}

arguments:
DBNAME               Name of Database

options:
-v, --verbose        Show info messages.
-d, --debug          Show debug messages.
-h, --help           Show this message and exit.
"""

class DBDump(Application):

    interface = Interface(PROGRAM, USAGE, HELP)

    dbname: str = ''
    interface.add_argument('dbname', nargs=1, default=dbname)

    debug: bool = False
    interface.add_argument('-d', '--debug', action='store_true')

    verbose: bool = False
    interface.add_argument('-v', '--verbose', action='store_true')

    def run(self) -> int:
        print(f'DEBUG: {self.debug}')
        print(f'VERBOSE: {self.verbose}')
        print(f'Dumo DB: {self.dbname}')

DBDump.__doc__ = __doc__

if __name__ == '__main__':
    import sys
    DBDump.main(sys.argv[1:])
