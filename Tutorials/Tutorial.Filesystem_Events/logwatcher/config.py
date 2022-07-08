from pathlib import Path
from dataclasses import dataclass

workdir = Path.cwd()
homedir = Path.home()

@dataclass
class WatchConfig(object):
    # The directory to Watch.
    WATCH_DIRECTORY: Path = homedir / 'log'

    # Delay time between Watch cycles in seconds.
    WATCH_INTERVAL: int = 1

    # allow to Watch into subdirectories.
    WATCH_RECURSIVELY: bool = False

    # To observate for WATCH_DIRECTORY
    WATCH_DO_OBSERVATE: bool = True

    # The suffix of watch files
    WATCH_FILE_SUFFIXES: str = '.txt, .log, .output'

    # The patterns for observations in watch files
    WATCH_PATTERN: str = "ERROR, FATAL"
