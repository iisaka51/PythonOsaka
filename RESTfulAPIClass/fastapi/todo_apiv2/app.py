from typing import List
from fastapi import Depends, FastAPI, HTTPException, Path
from fastalchemy import SQLAlchemyMiddleware, db
import models
import schemas
import crud

app = FastAPI()
app.add_middleware(SQLAlchemyMiddleware)

@app.get("/todo/api/v2.0/tasks/", response_model=List[schemas.TaskSchema])
def get_tasklist(skip: int = 0, limit: int = 100):
    tasklist = crud.get_tasklist(db, skip=skip, limit=limit)
    return tasklist

@app.get("/todo/api/v2.0/tasks/{id}")
def get_task(id: int):
    db_task = crud.get_task(db, task_id=id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/todo/api/v2.0/tasks")
def create_task(task: schemas.TaskSchema):
    return crud.create_task(db, task=task)

@app.patch("/todo/api/v2.0/tasks/{id}")
def patch_task(id: int, task: schemas.TaskSchema):
    db_task = crud.update_task(db, task_id=id, task=taask)
    return db_task

@app.delete("/todo/api/v2.0/tasks/{id}")
def delete_task(id: int):
    db_task = crud.delete_task(db, task_id=id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"result": "OK"}
