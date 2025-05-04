# 任务相关MySQL数据库操作
from sqlalchemy.orm import Session
from models import Task

def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_status(db: Session, task_id: int, status: str, output_image: str = None):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        if output_image:
            task.output_image = output_image
        db.commit()
        db.refresh(task)
    return task