"""
This is module POW.py
"""

class POW:
    def __init__(self, x=0, n=0):
        self.x = x
        self.n = n
        self.ans = self.pow(x, n)
    def __call__(self, x=None, n=None):
        self.ans = self.pow(x, n)
        return self
    def __str__(self):
        return(f'POW: x,n={self.x},{self.n}')

    def pow(self, x=None, n=None):
        if x == None and n == None:
            return self.ans
        if x == None:
            x = self.x
        if n == None:
            n = self.n
        try:
             self.ans = x ** n
             self.x, self.n = x, n
             return self.ans
        except ZeroDivisionError:
             print('cannot negative power')

if __name__ == '__main__':
    obj = POW(2,-3)
    print(obj)
    print(obj.pow())
    obj(4,2)
    print(obj.pow())
    print(obj(4,2).pow())
    print(obj.pow(2,3))
    obj.pow(0,-1)
