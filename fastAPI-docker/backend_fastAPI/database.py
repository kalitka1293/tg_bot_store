from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import load_dotenv
import os
from pathlib import Path

path_env = Path(os.path.dirname(__file__), '.env')
if os.path.exists(path_env):
    load_dotenv(path_env)
else:
    raise FileExistsError('Нет файла .env')

engine = create_async_engine(str(os.getenv('DATABASE')))

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
