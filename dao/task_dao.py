# 任务相关MySQL数据库操作
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Task

async def create_task(db: AsyncSession, task: Task):
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task_by_id(db: AsyncSession, task_id: int):
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_task_status(db: AsyncSession, task_id: int, status: str, output_image: str = None):
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    if task:
        task.status = status
        if output_image:
            task.output_image = output_image
        await db.commit()
        await db.refresh(task)
    return task