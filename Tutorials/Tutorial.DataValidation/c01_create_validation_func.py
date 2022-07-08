import re

class User:
    def __init__(self, id, username, email, age):
        self.id = id
        self.username = self.validate_name(username)
        self.email = self.validate_email(email)
        self.age = self.validate_age(age)

    def validate_name(self, val):
        if len(val) > 20:
            raise ValueError("Userame must be less than 20 characters.")
        return val

    def validate_email(self, val):
        regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
        if not re.match(regex, val):
            raise ValueError("Invalid email address.")
        return val

    def validate_age(self, val):
        if val < 0:
            raise ValueError("Age must be positive value.")
        return val

