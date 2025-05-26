from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Column
from app.schemas import ColumnCreate


async def get_columns(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Column).offset(skip).limit(limit))
    return result.scalars().all()


async def get_column(db: AsyncSession, column_id: int):
    result = await db.execute(select(Column).where(Column.id == column_id))
    return result.scalars().first()


async def get_columns_by_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Column).where(Column.project_id == project_id))
    return result.scalars().all()


async def create_column(db: AsyncSession, column: ColumnCreate):
    db_column = Column(**column.model_dump())
    db.add(db_column)
    await db.commit()
    await db.refresh(db_column)
    return db_column


async def update_column(db: AsyncSession, column_id: int, column_data: dict):
    result = await db.execute(select(Column).where(Column.id == column_id))
    db_column = result.scalars().first()

    if db_column:
        for key, value in column_data.items():
            setattr(db_column, key, value)
        await db.commit()
        await db.refresh(db_column)

    return db_column


async def delete_column(db: AsyncSession, column_id: int):
    result = await db.execute(select(Column).where(Column.id == column_id))
    db_column = result.scalars().first()

    if db_column:
        await db.delete(db_column)
        await db.commit()

    return db_column