from pydantic import BaseModel, StrictBool, ValidationError

class StrictBoolModel(BaseModel):
    strict_bool: StrictBool
