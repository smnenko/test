import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://baxity:baxity_secret@localhost:5432/baxity_test",
)

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:  # type: ignore[misc]
    async with async_session() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:  # type: ignore[misc]
    async with async_session() as session:
        async with session.begin():
            yield session
