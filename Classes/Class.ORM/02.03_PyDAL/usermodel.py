
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
        return( f'User: name:"{self.name}", age:{self.age}, belongs:"{self.belongs}"' )
