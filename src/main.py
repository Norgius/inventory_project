from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis


from api import create_api_app
from env_settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis_client = aioredis.from_url(str(settings.REDIS_DSN))
    app.state.redis_client = redis_client

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    await FastAPILimiter.init(redis_client)
    app.state.main_app = app.state

    yield

    await FastAPILimiter.close()
    await redis_client.close()


app = FastAPI(lifespan=lifespan)

app.mount('/api/v1', create_api_app(main_app_state=app.state))
