from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_async_engine("postgresql+asyncpg://tg:tg@localhost:5432/tg_store")

async_session = sessionmaker(
    engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=True,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
