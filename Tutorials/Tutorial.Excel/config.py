from pathlib import Path
from dataclasses import dataclass

workdir = Path.cwd()
homedir = Path.home()

@dataclass
class SpliterConfig(object):
    WORKSHEET: str = "Sheet1"
    MIN_ROW: int = 1
    MAX_ROW: int = 1000
    COLUMN: str = "A"
    DELIMITOR: str = ' '
