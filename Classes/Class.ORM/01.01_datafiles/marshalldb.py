from typing import Generic, List, TypeVar
from datafiles import Missing, converters, datafile
from datafiles.utils import dedent

data_dir = './datadir'
data_pattern = data_dir + '/marshalldb.yml'

S = TypeVar("S")
T = TypeVar("T")

class Pair(Generic[S, T], converters.Converter):
    first: S
    second: T

    def __init__(self, first: S, second: T) -> None:
        self.first = first
        self.second = second

    @classmethod
    def to_python_value(cls, deserialized_data, *, target_object=None):
        paired = zip(cls.CONVERTERS, deserialized_data)
        values = [convert.to_python_value(val) for convert, val in paired]
        return cls(*values)

    @classmethod
    def to_preserialization_data(cls, python_value, *, default_to_skip=None):
        values = [python_value.first, python_value.second]
        paired = zip(cls.CONVERTERS, values)
        return [
            convert.to_preserialization_data(val)
            for convert, val in paired
        ]

@datafile(data_pattern)
class Dictish:
    contents: List[Pair[str, converters.Number]]


if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
