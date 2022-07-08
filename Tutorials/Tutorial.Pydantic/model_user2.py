from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator

class User(BaseModel):
    id: int
    username : str
    password : str
    confirm_password : str
    email: str
    alias = 'anonymous'
    comment: str = ''
    timestamp: Optional[datetime] = None
    friends: List[int] = []

    @validator('id')
    def id_must_be_4_digits(cls, v):
        if len(str(v)) != 4:
            raise ValueError('must be 4 digits')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
