import re
from pygtail import Pygtail
from typing import List, Union

class FileChecker:
    def __init__(self, pattern: List[str]):
        if isinstance(pattern, list):
            self.pattern = pattern
        else:
            self.pattern = [pattern]

    def check_pattern(self, path: str ):
        for num, line in enumerate(Pygtail(path), 1):
            line = line.strip()
            if line:
                if any(re.findall('|'.join(self.pattern),
                        line, flags=re.IGNORECASE | re.VERBOSE)):
                    msg = (
                         f" File: {path},"
                         f" Found in line {num}: {line}"
                    )
                    yield msg
