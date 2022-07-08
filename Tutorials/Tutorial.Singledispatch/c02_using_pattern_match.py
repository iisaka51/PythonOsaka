from typing import Any, List

# Python 3.10

def fun(arg: Any) -> str:
    match arg:
        case int():
            return 'int'
        case list():
            return 'list'
        case _:
            return 'default'

assert fun(1) == 'int'
assert fun([]) == 'list'
assert fun('str') == 'default'
