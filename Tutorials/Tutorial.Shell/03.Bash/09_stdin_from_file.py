from bash import bash

with open('sample.txt') as fp:
    data = bash('cat', stdin=fp).value()

print(data)

