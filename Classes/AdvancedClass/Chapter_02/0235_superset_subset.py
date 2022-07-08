a = set([3, 2, 1])
b = set([5, 4, 3])
c = set([1, 2])
d = set([1, 2])

print('a :', a)
print('b :', b)
print('c :', c)
print('d :', d)

print('a > c :',a > c)
print('b > c :',b > c)
print('a > b :',a > b)
print('c > c :',c > c)

print('a >= c :',a >= c)    # a.issuperset(c)
print('b >= c :',b >= c)
print('a >= b :',a >= b)
print('c >= c :',c >= c)

print('a < c :',a < c)
print('b < c :',b < c)
print('a < b :',a < b)
print('c < c :',c < c)

print('a <= c :',a <= c)    # a.issubset(c)
print('b <= c :',b <= c)
print('a <= b :',a <= b)
print('c <= c :',c <= c)

print('d == d :',d == d)
print('d != d :',d != d)
print('c == d :',c == d)
print('c != d :',c != d)
