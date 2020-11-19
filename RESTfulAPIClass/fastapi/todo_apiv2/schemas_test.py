from pydantic import ValidationError
from schemas import TaskSchema

try:
    print(TaskSchema(title='just test'))
    print(TaskSchema())

except ValidationError as e:
    print(e.json())
