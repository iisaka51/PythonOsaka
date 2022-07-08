from snoop import pp

x = 1
y = 2

def debug():
    pp(pp(x + 1) + max(*pp(y + 2, y + 3)))

# debug()
