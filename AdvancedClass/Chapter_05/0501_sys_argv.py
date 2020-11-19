import sys

print('number of argument: ', len(sys.argv))
for n, arg in enumerate(sys.argv):
    print(f'argv[{n}] = {arg}')
print(__file__)

