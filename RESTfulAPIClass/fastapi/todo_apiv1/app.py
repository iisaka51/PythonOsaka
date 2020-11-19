from fastapi import FastAPI, HTTPException, Path
from tasks import tasks
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str = None
    done: bool = False

app = FastAPI()

@app.get("/todo/api/v1.0/tasks/{id}")
def get_task(
        id: int = Path(..., title="The ID of the task to get", gt=0)
    ):
    """This is GET REST API"""
    task = [task for task in tasks if task['id'] == id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    else:
        return {"data": task[0]}

@app.get("/todo/api/v1.0/tasks")
def get_tasklist():
    return {"data": tasks}

@app.post("/todo/api/v1.0/tasks")
def create_task(request_data: Task):
    tasks.append(request_data)
    return {"data": request_data}

@app.patch("/todo/api/v1.0/tasks/{id}")
def patch_task(
        id: int = Path(..., title="The ID of the task to get", gt=0)
    ):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    for key in request_data.keys():
        task[0][key] = request_data[key]
    return {"data": tasks[0]}

@app.delete("/todo/api/v1.0/tasks/{id}")
def delete_task(id: str):
    task_id = int(id)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    tasks.remove(task[0])
    return {"result": "OK"}
