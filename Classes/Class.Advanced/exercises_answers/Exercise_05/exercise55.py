from exercise52 import StrKeeper

class Validator(StrKeeper):
    def __init__(self):
        super().__init__()

    def validate(self, val, valstr, prompt='Input : ', retry=1, positive=True):
        while  retry > 0:
            retry -= 1
            if val == None:
                try:
                    val = float(self.getString(f'{prompt}'))
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

if __name__ == '__main__':
    obj = Validator()
    val = obj.validate(1, 'Val', 'Please input : ')
    print(val)
    val = obj.validate(-1, 'Val', 'Please input : ', retry=3, positive=True)
    print(val)
    val = obj.validate(None, 'Val', 'Please input : ', positive=True)
    print(val)
    val = obj.validate(-1, 'Val', 'Please input : ', positive=False)
    print(val)
