from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASS


async_engine = create_async_engine(
    # url="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
    url=f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False
)

async_session = async_sessionmaker(async_engine)


str_256 = Annotated[str, 256]