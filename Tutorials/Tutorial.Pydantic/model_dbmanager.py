from pydantic import (
    BaseModel,
    AnyUrl,
    SecretStr,
    EmailStr,
    ValidationError
    )
from ipaddress import IPv4Address

class DBServer(BaseModel):
    dsn: AnyUrl
    address: IPv4Address
    dbname: str
    dbuser: str
    passwd: SecretStr

class User(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr

