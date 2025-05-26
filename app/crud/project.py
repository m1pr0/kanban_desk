from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project  # Явный импорт модели
from app.schemas.project import ProjectCreate  # Явный импорт схемы


async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return result.scalars().all()


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalars().first()


async def create_project(db: AsyncSession, project: ProjectCreate):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def update_project(db: AsyncSession, project_id: int, project_data: dict):
    result = await db.execute(select(Project).where(Project.id == project_id))
    db_project = result.scalars().first()

    if db_project:
        for key, value in project_data.items():
            setattr(db_project, key, value)
        await db.commit()
        await db.refresh(db_project)

    return db_project


async def delete_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    db_project = result.scalars().first()

    if db_project:
        await db.delete(db_project)
        await db.commit()

    return db_project