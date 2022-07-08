from snoop import spy

def add_one(x):
    return x + 1

@spy
def myfunc(x, y):
    v =  add_one( x ) + ( y + 3 ) / x
    return v

def main():
    try:
        myfunc(0, 1)
    except:
        pass

# main()
