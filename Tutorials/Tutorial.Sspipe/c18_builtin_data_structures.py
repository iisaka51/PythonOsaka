X = 2
X = {X-1: [X, (X+1, 4)]}
print(X)


from sspipe import p, px
2 | p({px-1: p([px, p((px+1, 4))])}) | p(print)
