from abc import ABC, abstractmethod
import re

class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass

class Name(Validator):
    def __init__(self, minsize=8, maxsize=20):
        self.minsize = minsize
        self.maxsize = maxsize

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )

class Email:
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
        if not re.match(regex, value):
            raise ValueError(f'Expected {value!r} Invalid email address')

class Age(Validator):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected {value!r} to be an int')
        if value < 0:
            raise ValueError(f'Expected {value!r} to be positive value')


class User:

    username = Name(minsize=8, maxsize=20)
    email = Email()
    age = Age()

    def __init__(self, id, username, email, age):
        self.id = id
        self.username = username
        self.email = email
        self.age = age

