from typing import List
from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from database import get_db
import models
import schemas
import crud

app = FastAPI()
router = InferringRouter()

@cbv(router)
class TaskCBV:
    db: Session = Depends(get_db)

    @router.get("/todo/api/v2.0/tasks/")
    def get_tasklist(self, skip: int = 0, limit: int = 100):
        tasklist = crud.get_tasklist(self.db, skip=skip, limit=limit)
        return tasklist

    @router.get("/todo/api/v2.0/tasks/{id}")
    def get_task(self, id: int):
        db_task = crud.get_task(self.db, task_id=id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task

    @router.post("/todo/api/v2.0/tasks")
    def create_task(self, task: schemas.TaskSchema):
        return crud.create_task(self.db, task=task)

    @router.patch("/todo/api/v2.0/tasks/{id}")
    def patch_task(self, id: int, task: schemas.TaskSchema):
        db_task = crud.update_task(db, task_id=id, task=taask)
        return db_task

    @router.delete("/todo/api/v2.0/tasks/{id}")
    def delete_task(self, id: int):
        db_task = crud.delete_task(self.db, task_id=id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"result": "OK"}

app.include_router(router)
