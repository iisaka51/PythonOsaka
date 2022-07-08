import sys
from cmdkit.app import Application, ApplicationGroup, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace

APP_NAME = 'demo_simple'
APP_DESCRIPTION = """\
Description for demo application.
"""

APP_USAGE = f"""\
Usage: {APP_NAME} [-h|--help] price lots

{APP_DESCRIPTION}
"""

APP_HELP=f"""\
{APP_USAGE}

Options:
  -h, --help        show this message and exit.
"""

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    price: float = 0.0
    lots: int = 0

    interface.add_argument('price', type=float)
    interface.add_argument('lots', type=int)

    def run(self):
        print(f'{self.price} x {self.lots}')
        print(f'price: {type(self.price)}')
        print(f'lots: {type(self.lots)}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    v = main()
