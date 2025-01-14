from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app import Settings

settings = Settings()

# db_connection_str = settings.db_async_connection_str
# if "pytest" in modules:
#     db_connection_str = settings.db_async_test_connection_str

async_engine = create_async_engine(
    settings.db_async_connection_str,
    pool_size=20,
    pool_pre_ping=True,
    echo=settings.debug,
    max_overflow=20,
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
