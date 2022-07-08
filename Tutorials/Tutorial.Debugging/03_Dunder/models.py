class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return (f"User(first_name='{self.first_name}',"
                f"last_name='{self.last_name}')")

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}."

    def __bytes__(self):
        return bytes(str(self), 'utf-8')

    def __format__(self, format=None):
        if format == None:
            return str(self)
        else:
            return f'{format} is {str(self)}'
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.first_name == other.first_name and \
               self.last_name == other.last_name
    def __ne__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.first_name != other.first_name and \
               self.last_name != other.last_name

    def debug(self):
        print(f'Filename: {__file__}')
        print(f'FirstName: {self.first_name}')
        print(f'LastName: {self.last_name}')
