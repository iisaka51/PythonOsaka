# standard libs
from pathlib import Path

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface, ArgumentError
from cmdkit.config import Configuration

# internal libs
from config import workdir, homedir, WatchConfig

myconf = Configuration.from_local(
                 default = WatchConfig().__dict__,
                 env = False, prefix='',
                 user = str(homedir / '.logwatcher.yml'),
                 local = str(workdir / 'logwatcher.yml'))

APP_NAME='logwatcher'
APP_DESCRIPTION=f"""\
{APP_NAME} - Watchdog script for specified files and directories.
"""

APP_USAGE=f"""
{APP_DESCRIPTION}

Usage: {APP_NAME} [OPTIONS] <path>
"""

APP_HELP=f"""
{APP_USAGE}
Arguments:
 path             The path to Watch directory.
                  default is {myconf.WATCH_DIRECTORY}

Options:
-i, --interval    Watch interval seconds.
                  default is {myconf.WATCH_INTERVAL}
-O, --observate   Observate to watch directory.
                  default is {myconf.WATCH_DO_OBSERVATE}
-p, --pattern     Search pattern from logfiles in watch directory.
                  default is "{myconf.WATCH_PATTERN}"
-r, --recursive   Whether to recursively for subdirectories.
                  default is {myconf.WATCH_RECURSIVELY}
-s, --suffix      The suffixes for Watch directory.
                  default is "{myconf.WATCH_FILE_SUFFIXES}"
-h, --help        show this message and exit.
"""

def is_dir_path(path):
    if Path(path).is_dir():
        return path
    else:
        raise NotADirectoryError(path)

class MyApp(Application):

    ALLOW_NOARGS: bool = True
    interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

    path: Path = myconf.WATCH_DIRECTORY
    interval: int = myconf.WATCH_INTERVAL
    suffix: str = myconf.WATCH_FILE_SUFFIXES
    recursive: bool = myconf.WATCH_RECURSIVELY
    observate: bool = myconf.WATCH_DO_OBSERVATE
    pattern: bool = myconf.WATCH_PATTERN

    interface.add_argument('path', default=path, type=is_dir_path)
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
    try:
        MyApp.main(sys.argv[1:])
    except NotADirectoryError:
        print(APP_USAGE)
        print(f"<path> must be directory.")
        sys.exit(1)
