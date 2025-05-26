from fastapi import FastAPI
from app.routers import projects, columns, tasks
from app.core.database import engine, Base

app = FastAPI()

app.include_router(projects.router)
app.include_router(columns.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)