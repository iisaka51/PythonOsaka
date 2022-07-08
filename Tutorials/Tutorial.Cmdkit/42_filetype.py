import sys
from cmdkit.app import Application, ApplicationGroup, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace
import argparse
from typing import List, Union

APP_NAME = 'demo_simple'
APP_DESCRIPTION = """\
Description for demo application.
"""

APP_USAGE = f"""\
Usage: {APP_NAME} [-h|--help] [--infie path] [--outfile path]

{APP_DESCRIPTION}
"""

APP_HELP=f"""\
{APP_USAGE}

Options:
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    infile: argparse.FileType = None
    outfile: argparse.FileType = None

    interface.add_argument('--infile', type=argparse.FileType('r'))
    interface.add_argument('--outfile',
                           type=argparse.FileType('w', encoding='UTF-8'))

    def run(self):
        print(f'infile: {self.infile}')
        print(f'outile: {self.outfile}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
