from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Task, TaskLog
from app.schemas import TaskCreate, TaskLogCreate


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks_by_column(db: AsyncSession, column_id: int):
    result = await db.execute(select(Task).where(Task.column_id == column_id))
    return result.scalars().all()


async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    # Create log entry
    log = TaskLogCreate(
        task_id=db_task.id,
        message=f"Task created in column {db_task.column_id}"
    )
    await create_task_log(db, log)

    return db_task


async def update_task(db: AsyncSession, task_id: int, task_data: dict):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalars().first()

    if db_task:
        old_column_id = db_task.column_id
        for key, value in task_data.items():
            setattr(db_task, key, value)

        await db.commit()
        await db.refresh(db_task)

        # Create log entry if column changed
        if 'column_id' in task_data and old_column_id != db_task.column_id:
            log = TaskLogCreate(
                task_id=db_task.id,
                message=f"Task moved from column {old_column_id} to column {db_task.column_id}"
            )
            await create_task_log(db, log)

    return db_task


async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalars().first()

    if db_task:
        await db.delete(db_task)
        await db.commit()

    return db_task


async def get_task_logs(db: AsyncSession, task_id: int):
    result = await db.execute(select(TaskLog).where(TaskLog.task_id == task_id))
    return result.scalars().all()


async def create_task_log(db: AsyncSession, log: TaskLogCreate):
    db_log = TaskLog(**log.model_dump())
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log