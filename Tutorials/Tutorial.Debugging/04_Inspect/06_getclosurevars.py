import inspect

def stock():
    eqty  = 0

    def buy(price, log):
        return price * log
    return buy

print(inspect.getclosurevars(stock))
