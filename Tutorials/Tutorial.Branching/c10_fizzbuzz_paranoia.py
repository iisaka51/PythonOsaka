max = 100
ans = [ 'Fizz'*(n%3==0) + 'Buzz'*(n%5==0) or n for n in range(max + 1)]
