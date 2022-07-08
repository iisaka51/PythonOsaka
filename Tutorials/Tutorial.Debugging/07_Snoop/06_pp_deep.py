from snoop import pp

x = 1
y = 2

def debug():
    # pp(pp(x + 1) + max(*pp(y + 2, y + 3)))
    pp.deep(lambda: x + 1 + max(y + 2, y + 3))

# debug()
