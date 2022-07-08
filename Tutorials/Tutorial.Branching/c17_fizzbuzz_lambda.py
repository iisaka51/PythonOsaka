fizzbuzz = lambda n: ( "FizzBuzz" if n % 5 == 0 and n % 3 == 0 else
                       "Fizz" if n % 3 == 0 else
                       "Buzz" if n % 5 == 0 else n )

max = 100
ans = [ fizzbuzz(n) for n in range(1, max) ]
