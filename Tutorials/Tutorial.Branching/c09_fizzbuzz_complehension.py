max = 100
ans = [ 'FizzBuzz' if x % 5 == 0 and x % 3 == 0 else 'Buzz' if x % 5 == 0 else 'Fizz' if x % 3 == 0 else x for x in range(max+1)]
