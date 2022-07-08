# donot care ZeroDivisionError: 0.0 cannot be raised to a negative power

class POW:
    def __init__(self, x=0, n=0):
        self.ans = self.pow(x, n)
    def __call__(self, x=0, n=0):
        self.ans = self.pow(x, n)
        return self
    def __str__(self):
        return f'POW: x,n={self.x},{self.n}'
    def __pow(self, x, n):
        if x==0 or x==1 or n==1:
            return x
        if x==-1:
            if n%2 ==0:
                return 1
            else:
                return -1
        if n==0:
            return 1
        if n<0:
            return 1/self.__pow(x,-n)
        val = self.__pow(x,n//2)
        if n%2 ==0:
            return val*val
        return val*val*x
    def pow(self, x=None, n=None):
        if x == None:
            x = self.x
        if n == None:
            n = self.n
        self.ans =  self.__pow(x, n)
        self.x, self.n = x, n
        return self.ans

if __name__ == '__main__':
    obj = POW(2,-3)
    print(obj)
    print(obj.pow())
    obj(4,2)
    print(obj.pow())
    print(obj(4,2).pow())
    print(obj.pow(2,3))
    print(obj.pow(0,-1))

