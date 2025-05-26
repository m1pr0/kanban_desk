from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.core.config import settings

# Создаем асинхронный движок
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Создаем фабрику сессий с правильными типами
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор для получения сессии БД"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()