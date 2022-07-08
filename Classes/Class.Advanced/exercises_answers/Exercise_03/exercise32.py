def evenNumbers(maxval):
    return ( n for n in range(maxval) if n%2 == 0 )

maxval = int(input('Please input number: '))
for n in evenNumbers(maxval+1):
    print(n)
