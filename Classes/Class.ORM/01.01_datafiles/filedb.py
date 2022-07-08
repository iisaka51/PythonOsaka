from datafiles import *
from dataclasses import *
from typing import List

data_dir = './datadir'

@dataclass
class Nested:
    value: int

@dataclass
class Base:
    my_dict: Nested
    my_list: List[Nested]
    my_bool: bool = True
    my_float: float = 1.23
    my_int: int = 42
    my_str: str = "Hello, world!"

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
