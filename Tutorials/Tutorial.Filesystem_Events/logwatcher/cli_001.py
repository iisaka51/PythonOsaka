# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError

APP_NAME='logwatcher'
APP_DESCRIPTION=f"""\
{APP_NAME} - Watchdog script for specified directories.
"""

APP_USAGE=f"""
{APP_DESCRIPTION}

Usage: {APP_NAME} [OPTIONS] <path>
"""

APP_HELP=f"""
{APP_USAGE}
Arguments:
    path             The path to Watch directory.

Options:
    -i, --interval    Watch interval seconds.
    -O, --observate   Observate to watch directory.
    -p, --pattern     Search pattern from logfiles in watch directory.
    -r, --recursive   Whether to recursively for subdirectories.
    -s, --suffix      The suffixes for Watch directory.
    -h, --help        show this message and exit.
"""

class MyApp(Application):

    ALLOW_NOARGS: bool = True
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    path: str = ""
    interval: int = 1
    suffix: str = ".txt, .log"
    recursive: bool = False
    observate: bool = True
    pattern: str ="ERROR, FATAL"

    interface.add_argument('path', default=path, type=str)
    interface.add_argument('-i', '--interval', type=int,
                           default=interval )
    interface.add_argument('-r', '--recursive', action='store_true',
                           default=recursive )
    interface.add_argument('-s', '--suffix', type=str,
                           default=suffix )
    interface.add_argument('-w', '--observate', action='store_true',
                           default=observate )
    interface.add_argument('-p', '--pattern', type=str,
                           default=pattern )

    def run(self):
        print(f"path: {self.path}")
        print(f"interval: {self.interval}")
        print(f"suffix: {self.suffix}")
        print(f"recursive: {self.recursive}")
        print(f"observate: {self.observate}")
        print(f"pattern: {self.pattern}")


if __name__ == '__main__':
    import sys
    MyApp.main(sys.argv[1:])
