from check_prime import check_prime

def Primes(max):
    number = 1
    while number < max:
        number += 1
        if check_prime(number):
            yield number

primes = Primes(100)
for x in primes:
    print(x)
