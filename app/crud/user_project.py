from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models import UserProject


async def get_user_projects(db: AsyncSession, user_id: int):
    result = await db.execute(select(UserProject).where(UserProject.user_id == user_id))
    return result.scalars().all()


async def add_user_to_project(db: AsyncSession, user_id: int, project_id: int):
    db_user_project = UserProject(user_id=user_id, project_id=project_id)
    db.add(db_user_project)
    await db.commit()
    await db.refresh(db_user_project)
    return db_user_project


async def remove_user_from_project(db: AsyncSession, user_id: int, project_id: int):
    result = await db.execute(
        select(UserProject).where(
            and_(
                UserProject.user_id == user_id,
                UserProject.project_id == project_id
            )
        )
    )
    db_user_project = result.scalars().first()

    if db_user_project:
        await db.delete(db_user_project)
        await db.commit()

    return db_user_project