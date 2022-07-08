from pympler import asizeof
from dataclasses import dataclass
from collections import namedtuple
from typing import NamedTuple

simple_dict = dict(id=1, name='Freddie', part="Vocal",
                   email='freddie@example.com')

User1 = namedtuple('User1', "id name part email")
collection_namedtuple  = User1(id=1, name='Freddie', part="Vocal",
                              email='freddie@example.com')
class User2(NamedTuple):
    id: int
    name: str
    part: str
    email: str

typing_namedtuple  = User2(id=1, name='Freddie', part="Vocal",
                          email='freddie@example.com')

@dataclass
class User3(object):
    id: int
    name: str
    part: str
    email: str

@dataclass(frozen=True)
class User4(object):
    id: int
    name: str
    part: str
    email: str

dataclass_mutable  = User3(id=1, name='Freddie', part="Vocal",
                            email='freddie@example.com')
dataclass_immutable  = User4(id=1, name='Freddie', part="Vocal",
                            email='freddie@example.com')

comparison_data = {
    'simple_dict': simple_dict,
    'collection_namedtuple': collection_namedtuple,
    'typing_namedtuple': typing_namedtuple,
    'dataclass_mutable': dataclass_mutable,
    'dataclass_immutable': dataclass_immutable,
}

for key, val in comparison_data.items():
    print(f'{key}: {asizeof.asizeof(val)} bytes')
