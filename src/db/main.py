# src/db/main.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

# Using the native async engine to prevent connection drops with Neon
async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    connect_args={"timeout": 30, "command_timeout": 30},
)


async def init_db():
    async with async_engine.begin() as conn:
        # FIX: Import from their actual module paths where they are built!
        from src.db.models import Book, Review, User

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session_maker = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
