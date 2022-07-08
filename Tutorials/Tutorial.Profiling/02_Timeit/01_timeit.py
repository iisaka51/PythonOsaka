from timeit import timeit

test_code = '"-".join(str(n) for n in range(1000))'
test = timeit(test_code, number=100)

print(f'{test}')
