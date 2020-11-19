from sqlalchemy.orm import Session
import models
import schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasklist(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskSchema):
    db_task = models.Task(title=task.title,
                       description=task.description,
                       done=task.done)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskSchema):
    db_task = get_task(task_id=task_id, db=db)
    if db_task is not None:
        db_task.title = task.tiel
        db_task.description = task.description
        db_task.done = task.done
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(task_id=task_id, db=db)
    if db_task is not None:
        db.delete(db_task)
        db.commit()
        db.refresh(db_task)
    return db_task
