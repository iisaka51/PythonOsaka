import os
import sys
from cmdkit.app import Application, ApplicationGroup, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace

APP_NAME = 'demo_simple'
APP_DESCRIPTION = """\
Description for demo application.
"""

APP_USAGE = f"""\
Usage: {APP_NAME} [-h|--help] [-U|--user username]  name

{APP_DESCRIPTION}
"""

APP_HELP=f"""\
{APP_USAGE}

Options:
  -U, --user        set username
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    name: str = 'Python'
    username: str = os.getlogin()

    interface.add_argument('name', nargs='?', default=name)
    interface.add_argument('-U', '--username', default=username)

    def run(self):
        print(f'USER: {self.username}')
        print(f'Hello {self.name}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
