from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas import Column, ColumnCreate, ColumnUpdate
from app.crud import column as crud
from app.core.database import get_db

router = APIRouter(prefix="/columns", tags=["columns"])

@router.post("/", response_model=Column)
async def create_column(column: ColumnCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_column(db, column)

@router.get("/", response_model=List[Column])
async def read_columns(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    columns = await crud.get_columns(db, skip=skip, limit=limit)
    return columns

@router.get("/{column_id}", response_model=Column)
async def read_column(column_id: int, db: AsyncSession = Depends(get_db)):
    db_column = await crud.get_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return db_column

@router.get("/project/{project_id}", response_model=List[Column])
async def read_columns_by_project(project_id: int, db: AsyncSession = Depends(get_db)):
    columns = await crud.get_columns_by_project(db, project_id=project_id)
    return columns

@router.put("/{column_id}", response_model=Column)
async def update_column(column_id: int, column: ColumnUpdate, db: AsyncSession = Depends(get_db)):
    db_column = await crud.update_column(db, column_id, column.model_dump(exclude_unset=True))
    if db_column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return db_column

@router.delete("/{column_id}", response_model=Column)
async def delete_column(column_id: int, db: AsyncSession = Depends(get_db)):
    db_column = await crud.delete_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return db_column