from datetime import datetime
from typing import List, Optional
from pydantic import (
    BaseModel, EmailStr, SecretStr,
    ValidationError, validator
    )

class Beer:
    name: str
    abv: float   # Alcohol by Volume (アルコール度数)

@datafile(data_pattern)
class Drink:
    brewery: str
    data: Beer
