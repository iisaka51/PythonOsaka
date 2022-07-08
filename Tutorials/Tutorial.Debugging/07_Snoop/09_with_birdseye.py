from snoop import snoop
from birdseye import eye


def add_one(x):
    return x + 1

@snoop
@eye
def myfunc(x, y):
    v =  add_one( x ) + ( y + 3 ) / x
    return v

def main():
    try:
        myfunc(0, 1)
    except:
        pass

# main()

# Run birdseye or python -m birdseye  on other terminal
# Open http://localhost:7777 in your browser
