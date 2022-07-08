max = 100

for n in range(1, max):
    match n:
        case _ if n % 5 == 0 and n % 3 == 0: print('FizzBuzz')
        case _ if n % 3 == 0: print('Fizz')
        case _ if n % 5 == 0: print('Buzz')
        case _: print(n)
