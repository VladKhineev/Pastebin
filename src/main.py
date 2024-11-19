from fastapi import FastAPI

from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import os
import sys

from src.user.routers import router as router_user
from src.post.routers import router as router_post
from src.task.routers import router as router_task

from src.config import REDIS_HOST, REDIS_PORT


# sys.path.insert(1, os.path.join(sys.path[0], '..'))

async def lifespan(app: FastAPI):
    '''Подключаем все необходимые инструменты до поднятия сервера'''
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(title='Pastebin', lifespan=lifespan)

app.include_router(router_user)
app.include_router(router_post)
app.include_router(router_task)