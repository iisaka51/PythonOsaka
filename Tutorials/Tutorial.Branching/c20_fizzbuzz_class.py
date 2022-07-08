from typing import Union, Tuple

class FizzBuzz:
    def __init__(self, n: int):
        self.n: int = n
        self._fizzbuzz: Union[str, int] = (
            "FizzBuzz" if self.n % 5 == 0 and self.n % 3 == 0 else
            "Fizz" if self.n % 3 == 0 else
            "Buzz" if self.n % 5 == 0 else self.n )

    @property
    def fizzbuzz(self) -> Tuple[int, Union[str, int]]:
        return self.n, self._fizzbuzz

max = 100
ans = [ FizzBuzz(n) for n in range(1, max)]
