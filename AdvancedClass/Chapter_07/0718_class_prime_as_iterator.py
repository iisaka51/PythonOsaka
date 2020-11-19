from check_prime import check_prime

class Primes:
    def __init__(self, max):
        self.max = max
        self.number = 1
    def __iter__(self):
        return self
    def __next__(self):
        self.number += 1
        if self.number >= self.max:
            raise StopIteration
        elif check_prime(self.number):
            return self.number
        else:
            return self.__next__()

primes = Primes(100)
for x in primes:
    print(x)
