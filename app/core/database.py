import sys

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app import Settings

settings = Settings()


def get_db_url() -> str:
    if "pytest" in sys.modules:
        return settings.db_async_connection_str_test
    return settings.db_async_connection_str


async_engine = create_async_engine(
    get_db_url(),
    pool_size=20,
    pool_pre_ping=True,
    echo=settings.debug,
    max_overflow=20,
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
