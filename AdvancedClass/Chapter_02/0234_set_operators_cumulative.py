a = set([3, 2, 1])
b = set([5, 4, 3])

a |= b           # a = a | b
print(a)
a &= b           # a = a & b
print(a)
a -= b           # a = a - b
print(a)
a ^= b           # a = a ^ b
print(a)
