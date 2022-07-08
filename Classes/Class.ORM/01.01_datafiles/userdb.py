from datafiles import *
from typing import List
from dataclass_type_validator import (
    dataclass_type_validator, TypeValidationError
    )

@datafile("userdb/{self.id}.yml")
class User:

    id: int
    name: str
    friend_ids: List[int]

    def __post_init__(self):
        dataclass_type_validator(self)
