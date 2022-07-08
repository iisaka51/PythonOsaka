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
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    ALLOW_NOARGS = True
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    name: str = 'Python'
    interface.add_argument('name', nargs='?', default=name)

    def run(self):
        print(f'Hello {self.name}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
