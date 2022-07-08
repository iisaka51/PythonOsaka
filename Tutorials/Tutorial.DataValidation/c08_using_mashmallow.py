from marshmallow import Schema, fields, validate, ValidationError
from dataclasses import dataclass, asdict
from test_data import users

class UserSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1))
    username = fields.Str(validate=validate.Length(max=20))
    email = fields.Email()
    age = fields.Integer(validate=validate.Range(min=1))

@dataclass
class User:
    id: int
    username: str
    email: str
    age: int


user = User(**users[0])
data = UserSchema().load(asdict(user))

user.username = "Goichi (iisaka) Yukawa"
user.age = -20
try:
    data = UserSchema().load(asdict(user))
except ValidationError as e:
    print(e)
