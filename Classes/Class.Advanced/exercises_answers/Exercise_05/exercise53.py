from exercise52 import StrKeeper

class Rectangle(StrKeeper):
    def __init__(self, length=None, width=None):
        super().__init__()
        self.length = self.validate(length, 'Length', 'Input Length: ')
        self.width = self.validate(width, 'Width', 'Input Width: ')

    def __call__(self, length=0, width=0):
        self.length = self.validate(length, 'Length', 'Length', retry=3)
        self.width = self.validate(width, 'Width', 'Width', retry=3)
        return self

    def validate(self, val, valstr, prompt, retry=3, positive=True):
        while  retry > 0:
            retry -= 1
            if val == None:
                try:
                    val = int(self.getString(f'{prompt} :'))
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
        return self.length * self.width

if __name__ == '__main__':
    obj = Rectangle(3,3)
    print(obj.area())
    print(obj(4,3).area())
    obj = Rectangle()
    print(obj.area())
