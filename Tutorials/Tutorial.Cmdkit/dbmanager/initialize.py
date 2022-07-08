"""Initialize database """

import sys
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface
from .dblogging import log

NAME = 'initialize'
PROGRAM = 'dbmanager initialize'
PADDING = ' ' * len(PROGRAM)

USAGE = f"""\
       {PROGRAM} FILE
       {PADDING} [--verbose] [--debug]
       {PADDING} [--help]

"""

HELP = f"""\
{USAGE}

arguments:
FILE                 Path to file for database

options:
-v, --verbose        Show info messages.
-d, --debug          Show debug messages.
-h, --help           Show this message and exit.
"""

class DBInit(Application):

    interface = Interface(PROGRAM, USAGE, HELP)

    dbfile: str = ''
    interface.add_argument('dbfile', nargs=1, default=dbfile)

    debug: bool = False
    interface.add_argument('-d', '--debug', action='store_true')

    verbose: bool = False
    interface.add_argument('-v', '--verbose', action='store_true')

    def run(self) -> int:
        print(f'DEBUG: {self.debug}')
        print(f'VERBOSE: {self.verbose}')
        print(f'DB initialize DB: {self.dbfile}')

DBInit.__doc__ = __doc__

if __name__ == '__main__':
    DBInit.main(sys.argv[1:])
