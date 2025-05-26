from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    column_id: int
    project_id: int


class TaskUpdate(TaskBase):
    column_id: Optional[int] = None


class Task(TaskBase):
    id: int
    column_id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskLogBase(BaseModel):
    message: str


class TaskLogCreate(TaskLogBase):
    task_id: int


class TaskLog(TaskLogBase):
    id: int
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True