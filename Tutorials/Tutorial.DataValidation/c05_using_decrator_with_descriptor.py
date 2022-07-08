from c003_using_descriptors import Name, Email, Age

def email(attr):
    def decorator(cls):
        setattr(cls, attr, Email())
        return cls
    return decorator

def age(attr):
    def decorator(cls):
        setattr(cls, attr, Age())
        return cls
    return decorator

def name(attr):
    def decorator(cls):
        setattr(cls, attr, Name())
        return cls
    return decorator

@email("email")
@age("age")
@name("username")
class User:
    def __init__(self, id, username, email, age):
        self.id = id
        self.username = username
        self.email = email
        self.age = age
