class User:
    nme: str
    age: int
    belongs: str

    def __init__(self, profile: dict):
        self.data = dict(profile)
        self.name = self.data['name']
        self.age = int(self.data['age'])
        self.belongs = self.data['belongs']

    def __repr__(self):
        return( f'User(name="{self.name}", '
                f'"age=age:{self.age}", '
                f'belongs=belongs:"{self.belongs}")' )

    def __spr__(self):
        return f'User:"{self.name}", age:{self.age}, "{self.belongs}"'

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.name == other.name and \
               self.age == other.age and \
               self.belongs == other.belongs
