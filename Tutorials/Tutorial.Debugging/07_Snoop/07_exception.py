from snoop import pp

x = 0
y = 2

def debug():
    pp.deep(lambda: x + 1 + (y + 3) / x)

# debug()
