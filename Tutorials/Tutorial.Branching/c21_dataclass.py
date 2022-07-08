from dataclasses import dataclass, field
from typing import Union

@dataclass
class Number:
    n: int
    fizzbuzz: Union[str, int] = field(init=False)

    def __post_init__(self) -> None:
        self.fizzbuzz = (
            "FizzBuzz" if self.n % 5 == 0 and self.n % 3 == 0 else
            "Fizz" if self.n % 3 == 0 else
            "Buzz" if self.n % 5 == 0 else self.n )

max = 100
ans = [ Number(n) for n in range(1, max)]

