def fizzbuzz(n):
    data  = ( "FizzBuzz" if n % 5 == 0 and n % 3 == 0 else
              "Fizz" if n % 3 == 0 else
              "Buzz" if n % 5 == 0 else n )
    return data

max = 100
ans = [ fizzbuzz(n) for n in range(1, max) ]
