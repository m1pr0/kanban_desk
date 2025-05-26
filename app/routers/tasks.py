from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas import Task, TaskCreate, TaskUpdate, TaskLog
from app.crud import task as crud
from app.core.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task)

@router.get("/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/column/{column_id}", response_model=List[Task])
async def read_tasks_by_column(column_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await crud.get_tasks_by_column(db, column_id=column_id)
    return tasks

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await crud.update_task(db, task_id, task.model_dump(exclude_unset=True))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=Task)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/{task_id}/logs", response_model=List[TaskLog])
async def read_task_logs(task_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_task_logs(db, task_id=task_id)