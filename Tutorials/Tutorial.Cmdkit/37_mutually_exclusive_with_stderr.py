import sys
import functools
from typing import Callable
from cmdkit.app import Application, exit_status, log
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
      --disable      Set disable. not allowed with argument --enable
  -D, --debug       debug mode
  -v, --verbose     print message verbosly
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    debug: bool = False
    verbose: int = 0
    log_critical = functools.partial(print, file=sys.stderr)
    log_exception = functools.partial(print, file=sys.stderr)

    interface.add_argument('-D', '--debug',
                           default=debug, action='store_true')

    interface.add_argument('-v', '--verbose',
                           default=verbose, action='count')

    enable: bool = False
    disable: bool = False
    group = interface.add_mutually_exclusive_group()
    group.add_argument('--enable', action='store_true')
    group.add_argument('--disable', action='store_true')

    def run(self):
        print(f'DEBUG: {self.debug}')
        print(f'VERBSE: {self.verbose}')
        print(f'enable: {self.enable}')
        print(f'disable: {self.disable}')


def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
