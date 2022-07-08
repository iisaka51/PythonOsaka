from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username : str
    password : str
    confirm_password : str
    email: str
    alias = 'anonymous'
    timestamp: Optional[datetime] = None
    friends: List[int] = []
