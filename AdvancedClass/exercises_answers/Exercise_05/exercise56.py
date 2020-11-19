from exercise55 import Validator

class Rectangle(Validator):
    def __init__(self, length=None, width=None):
        super().__init__()
        self.length = self.validate(length, 'Length', 'Length', retry=3)
        self.width = self.validate(width, 'Width', 'Width', retry=3)

    def __call__(self, length=0, width=0):
        self.length = self.validate(length, 'Length', 'Length', retry=3)
        self.width = self.validate(width, 'Width', 'Width', retry=3)
        return self

    def area(self):
        return self.length * self.width

if __name__ == '__main__':
    obj = Rectangle(3,3)
    print(obj.area())
    print(obj(4,3).area())
    obj = Rectangle()
    print(obj.area())
