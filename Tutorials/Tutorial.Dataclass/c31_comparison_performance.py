from time import perf_counter
from dataclasses import dataclass, astuple
from collections import namedtuple
from typing import NamedTuple

def average_time(count, data, func):
    sampling = []
    for _ in range(count):
        start = perf_counter()
        func(data)
        end = perf_counter()
        sampling.append(end - start)
    result = sum(sampling) / count * int(1e8)
    return result

def perfcheck_dict(dictionary):
    _ = "name" in dictionary
    _ = "missing" in dictionary
    _ = "Freddie" in dictionary.values()
    _ = "missing" in dictionary.values()
    _ = dictionary["name"]

def perfcheck_namedtuple(named_tuple):
    _ = "name" in named_tuple._fields
    _ = "missing" in named_tuple._fields
    _ = "Freddie" in named_tuple
    _ = "missing" in named_tuple
    _ = named_tuple.name

def perfcheck_dataclass(data_class):
    _ = "name" in data_class.__dict__
    _ = "missing" in data_class.__dict__
    _ = "Freddie" in data_class.__repr__()
    _ = "missing" in data_class.__repr__()
    _ = data_class.name

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

def main():
    test_count = 1_000_000
    time_of_dict = average_time(test_count,
                         simple_dict, perfcheck_dict)
    time_of_col_namedtuple = average_time(test_count,
                         collection_namedtuple, perfcheck_namedtuple)
    time_of_typing_namedtuple = average_time(test_count,
                            typing_namedtuple, perfcheck_namedtuple)
    time_of_dataclass_mutable = average_time(test_count,
                            dataclass_mutable, perfcheck_dataclass)
    time_of_dataclass_immutable = average_time(test_count,
                            dataclass_immutable, perfcheck_dataclass)

    print(f'                dict: {time_of_dict}')
    print(f'collection_namedtupe: {time_of_col_namedtuple}')
    print(f'   typing_namedtuple: {time_of_typing_namedtuple}')
    print(f'   dataclass mutable: {time_of_dataclass_mutable}')
    print(f' dataclass immutable: {time_of_dataclass_immutable}')

