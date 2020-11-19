from pydantic import Field, BaseModel
from fastapi_utils.api_model import APIModel

class TaskSchema(APIModel):
    id: int = Field(None)
    title: str = Field(...,
                       title='The title of task',
                       max_length=32)
    description: str = Field(None,
                       title='The description of task',
                       max_length=128)
    done: bool = Field(False, title='The status of task')

    class config:
        orm_mode = True
