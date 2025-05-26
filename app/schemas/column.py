from pydantic import BaseModel
from typing import Optional


class ColumnBase(BaseModel):
    title: str
    order: Optional[int] = 0


class ColumnCreate(ColumnBase):
    project_id: int


class ColumnUpdate(ColumnBase):
    pass


class Column(ColumnBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True