import re

class User:
    def __init__(self, id, username, email, age):
        self._id = id
        self._username = username
        self._email = email
        self._age = age

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if len(value) > 20:
            raise ValueError("Userame must be less than 20 characters.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
        if not re.match(regex, value):
            raise ValueError("Invalid email address.")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age musst be postive value.")
        self._age = value

