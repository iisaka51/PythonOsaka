!cat datadir/sample.yml

from datafiles import auto

sample = auto('datadir/sample.yml')
v1 = sample.names

sample.numbers.append(3)


# print(v1)
# !cat datadir/sample.yml
