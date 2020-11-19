from exercise51 import POW
from exercise55 import Validator

class Circle(Validator, POW):
    def __init__(self, radius=None):
        super().__init__()
        self.__hidden_pi = 3.141592653589793
        self.radius = self.validate(radius, 'Radius', 'Radius ', retry=3, positive=True)
    def __call__(self, radius=0):
        self.radius = self.validate(radius, 'Radius', 'Radius ', retry=3, positive=True)
        return self

    def setpi(self,dummy=0):
        self.__hidden_pi = 3.141592653589793

    def getpi(self):
        return self.__hidden_pi

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
