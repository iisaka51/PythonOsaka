import sys
from cmdkit.app import Application, ApplicationGroup, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace

APP_NAME = 'demo_simple'
APP_DESCRIPTION = """\
Description for demo application.
"""

APP_USAGE = f"""\
Usage: {APP_NAME} [-h|--help] [name]

{APP_DESCRIPTION}
"""

APP_HELP=f"""\
{APP_USAGE}

Options:
      --enable      Set enable. not allowed with argument --disable
      --diable      Set disable. not allowed with argument --enable
  -D, --debug       debug mode
  -v, --verbose     print message verbosly
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    debug: bool = False
    verbose: int = 0
    mode: bool = True

    interface.add_argument('-D', '--debug',
                           default=debug, action='store_true')
    interface.add_argument('-v', '--verbose',
                           default=verbose, action='count')

    interface.add_argument('--enable', dest='mode',
                       default=mode, action='store_true')
    interface.add_argument('--disable', dest='mode',
                       default=mode, action='store_false')

    def run(self):
        print(f'DEBUG: {self.debug}')
        print(f'VERBSE: {self.verbose}')
        print(f'MODE: {self.mode}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
