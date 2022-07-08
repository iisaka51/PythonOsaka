import fnc

BEER = 0
@fnc.retry(attempts=4, delay=2)
def drink_beers():
    global BEER
    BEER += 1
    print(f'I drink {BEER} paint of beers')
    raise Exceptions('retry count exceeded')

try:
    drink_beers()
except Exception:
    pass
