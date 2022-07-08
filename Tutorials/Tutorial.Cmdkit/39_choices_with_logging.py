import sys
from cmdkit.app import Application, ApplicationGroup, exit_status, log
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Namespace
import logging

# 標準出力(コンソール)にログを出力するハンドラを生成する
log_stderr = logging.StreamHandler(sys.stderr)
log_stderr.setLevel(logging.WARNING)
log_stderr.setLevel(logging.CRITICAL)

# ハンドラをロガーに紐づける
log.addHandler(log_stderr)

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

class DemoApp(Application):
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    name: str = 'Python'
    color: str = 'green'

    interface.add_argument('name', nargs='?', default=name)
    interface.add_argument('-c', '--color', default=color,
                           choices=['green', 'yellow', 'red'])

    def run(self):
        print(f'COLOR: {self.color}')
        print(f'Hello {self.name}')

def main() -> int:
    return DemoApp.main(sys.argv[1:])

if __name__ == '__main__':
    main()
