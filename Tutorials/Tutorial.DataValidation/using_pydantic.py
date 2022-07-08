from pydantic import (
         BaseModel, ValidationError, validator, PositiveInt, EmailStr
     )

class User(BaseModel):
    id: str
    username: str
    birthday: str
    email: EmailStr
    age: PositiveInt

    @validator('birthday')
    def valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("date must be in YYYY-MM-DD format.")

try:
    user = User(
        id=1,
        name="Goichi Iisaka Yukawa",
        birthday="1962-01-13",
        email="iisaka51@example...",
        age=-2,
    )
    print(user)
except ValidationError as e:
    print(e)
