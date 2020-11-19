def evenNumbers(maxval):
    nums = list()
    for n in range(maxval):
        if n%2 == 0:
            yield n


maxval = int(input('Please input number: '))
for n in evenNumbers(maxval+1):
    print(n)
