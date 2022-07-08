import re

class Name:
    def __get__(self, obj, value=None):
        return self.value

    def __set__(self, obj, value):
        if len(value) > 20:
            raise ValueError("Userame must be less than 20 characters.")
        self.value = value

class Email:
    def __get__(self, obj, value=None):
        return self.value

    def __set__(self, obj, value):
        regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
        if not re.match(regex, value):
            raise ValueError("Invalid email address.")
        self.value = value

class Age:
    def __get__(self, obj, value=None):
        return self.value

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Age must be postive value.")
        self.value = value

class User:

    name = Name()
    email = Email()
    age = Age()

    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

