from typing import Annotated

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASS


static_engine = create_engine(
    # url="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
    url=f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False
)

# connection check
# with static_engine.connect() as conn:
#     res = conn.execute(text('select version()'))
#     print(f'{res=}')


static_session = sessionmaker(static_engine)


str_256 = Annotated[str, 256]