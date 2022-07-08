import sys
from cmdkit.app import Application, ApplicationGroup, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace
import argparse

APP_NAME = 'demo_simple'
APP_DESCRIPTION = """\
Description for demo application.
"""

APP_USAGE = f"""\
Usage: {APP_NAME} [-h|--help] [-c|--color <green|yellow|red>]  name

{APP_DESCRIPTION}
"""

APP_HELP=f"""\
{APP_USAGE}

Options:
  -h, --help        show this message and exit.
"""

class ChoiceAction(argparse.Action):
    ACCEPTABLE_CHOICES=['green', 'yellow', 'red']
    def __call__(self, parser, namespace, values=None, options_string=None):
        if values is not None and values in self.ACCEPTABLE_CHOICES:
            setattr(namespace, self.dest, values)
        else:
            print(f"invalid {values} in {self.ACCEPTABLE_CHOICES}")
            print(APP_USAGE)
            sys.exit(exit_status.bad_argument)

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    name: str = 'Python'
    color: str = 'green'

    interface.add_argument('name', nargs='?', default=name)
    interface.add_argument('-c', '--color', nargs='?', default=color,
                           action=ChoiceAction)

    def run(self):
        print(f'COLOR: {self.color}')
        print(f'Hello {self.name}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
