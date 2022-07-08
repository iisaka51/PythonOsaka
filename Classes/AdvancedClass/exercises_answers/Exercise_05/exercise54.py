from exercise51 import POW
from exercise52 import StrKeeper

class Circle(StrKeeper, POW):
    def __init__(self, radius=None):
        super().__init__()
        self.__hidden_pi = 3.141592653589793
        self.radius = self.validate(radius)

    def __call__(self, radius=0):
        self.radius = self.validate(radius)
        return self

    def setpi(self,dummy=0):
        self.__hidden_pi = 3.141592653589793

    def getpi(self):
        return self.__hidden_pi

    def validate(self, val=None, valstr='Radius', prompt='Radius : ', retry=3, positive=True):
        while  retry > 0:
            retry -= 1
            if val == None:
                try:
                    val = int(self.getString(f'{prompt}'))
                except ValueError as msg:
                    print(msg)
                    val = None
                    continue
            if positive and val < 0:
                print(f'{valstr} must be set positive value')
                val = None
                continue
            break
        else:
            raise(ValueError(f'{valstr} must be set positive value'))
        return val

    def area(self):
        return float(self.pow(float(self.radius), 2)) * self.pi

    pi = property(getpi, setpi)

if __name__ == '__main__':
    obj = Circle(3)
    print(obj.pi)
    obj.pi = 3.14
    print(obj.pi)
    print(obj.area())
    print(obj(4).area())

    obj = Circle()
    print(obj.area())
