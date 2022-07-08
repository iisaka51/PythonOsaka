from typing import Union

def add(first_value: int, second_value: int) -> Union[int, bool]:
    if first_value == 0:
        return False
    return first_value + second_value

print(add(1,10))
