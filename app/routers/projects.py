from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas import Project, ProjectCreate, ProjectUpdate
from app.crud import project as crud
from app.crud import user_project as user_crud
from app.core.database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project(db, project)

@router.get("/", response_model=List[Project])
async def read_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    projects = await crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=Project)
async def read_project(project_id: int, db: AsyncSession = Depends(get_db)):
    db_project = await crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    db_project = await crud.update_project(db, project_id, project.model_dump(exclude_unset=True))
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}", response_model=Project)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    db_project = await crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.post("/{project_id}/users/{user_id}")
async def add_user_to_project(project_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_crud.add_user_to_project(db, user_id, project_id)

@router.delete("/{project_id}/users/{user_id}")
async def remove_user_from_project(project_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_crud.remove_user_from_project(db, user_id, project_id)