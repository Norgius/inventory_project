from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi import Limiter
from slowapi.util import get_remote_address

from app_context import limiter_var
from env_settings import settings

limiter = Limiter(key_func=get_remote_address)
limiter_var.set(limiter)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if settings.REDIS_DSN:
        redis_client = aioredis.from_url(str(settings.REDIS_DSN))
        app.state.redis_client = redis_client
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    else:
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    app.state.main_app = app.state

    yield

    if settings.REDIS_DSN:
        await redis_client.close()


app = FastAPI(lifespan=lifespan)

from api import create_api_app  # noqa: E402

app.mount('/api/v1', create_api_app(main_app_state=app.state))
