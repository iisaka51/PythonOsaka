X = range(5)
X = filter((lambda x:x%2==0),X)
X = map((lambda x: x + 10), X)
X = list(X)
print(X)


from sspipe import p, px
( range(5)
  | p(filter, px % 2 == 0)
  | p(map, px + 10)
  | p(list) | p(print)
)
