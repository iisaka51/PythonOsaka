import sys
from cmdkit.app import ApplicationGroup
from cmdkit.cli import Interface, ArgumentError

# commands
from .initialize import DBInit
from .dump import DBDump
from .dblogging import log

COMMANDS = {
    'initialize': DBInit,
    'dump': DBDump,
}

PROGRAM = 'dbmanager'

USAGE = f"""\
usage: {PROGRAM} <command> [<args>...]
       {PROGRAM} [--help]

database manager.
"""

HELP = f"""\
{USAGE}\

commands:
initialize             {DBInit.__doc__}
dump                   {DBDump.__doc__}

options:
-h, --help             Show this message and exit.

Use the -h/--help flag with the above commands to
learn more about their usage.

"""

class CompletedCommand(Exception):
    pass

class DBManager(ApplicationGroup):
    interface = Interface(PROGRAM, USAGE, HELP)

    command: str = None
    interface.add_argument('command')

    exceptions = {
        CompletedCommand: (lambda exc: int(exc.args[0])),
    }


    def run(self) -> None:
        try:
            status = COMMANDS[self.command].main(sys.argv[2:])
            raise CompletedCommand(status)

        except KeyError as error:
            cmd, = error.args
            raise ArgumentError(f'"{cmd}" is not an available command.')

def main() -> int:
    return DBManager.main(sys.argv[1:])


if __name__ == '__main__':
    import sys
    sys.exit(main())
