import asyncio

import pytest
from typing import AsyncGenerator

from src.config import MODE
from src.database import async_engine
from src.models import Base

from httpx import ASGITransport, AsyncClient
from src.main import app



@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    assert MODE == 'TEST'

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop() -> AsyncGenerator:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac