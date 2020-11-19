from fastapi import FastAPI, HTTPException
from tasks import tasks

app = FastAPI()

@app.get("/todo/api/v1.0/tasks/{id}")
def get_task(id):
    try:
        task_id = int(id)
        return {"data": tasks[task_id]}
    except:
        raise HTTPException(status_code=404, detail="Not found")

@app.get("/todo/api/v1.0/tasks")
def get_tasklist(id=None):
    return {"data": tasks}

@app.post("/todo/api/v1.0/tasks")
def create_task(request_data: dict):
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request_data['title'],
        'description': request_data['description'],
        'done': False
    }
    tasks.append(task)
    return {"data": request_data}

@app.patch("/todo/api/v1.0/tasks/{id}")
def patch_task(id: str, request_data: dict):
    task_id = int(id)
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
