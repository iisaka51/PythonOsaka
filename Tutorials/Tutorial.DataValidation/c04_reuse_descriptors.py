from c03_using_descriptors import Name, Email, Age

class Salary:
    def __get__(self, obj):
        self.value

    def __set__(self, obj, value):
        if value < 1000:
            raise ValueError("Salary must be upper than 1000.")
        self.value = value

class Employee:
    name = Name()
    email = Email()
    age = Age()
    salary = Salary()

    def __init__(self, id, name, email, age, salary):
        self.id = id
        self.name = name
        self.email = email
        self.age = age
        self.salary = salary

users = [
    dict(id=1, name="Jack Johnson",
         email="jackJohnson@example.com",
         age=40, salary=1000),
    dict(id=2, name="Eddie Jackson",
         email="edduiejackson@example.com",
         age=-20, salary=1000),
    dict(id=3, name="Goichi longlong name iisaka",
         email="iisaka51@example.com",
         age=60, salary=200),
]

# person = Employee(**users[0])
# person = Employee(**users[1])
# person = Employee(**users[2])
