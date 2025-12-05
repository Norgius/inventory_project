import json
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.asyncio.client import Redis

from env_settings import settings

from ._error_messages import IDEMPOTENCY_KEY_NOT_FOUND
from .utils import key_builder


def find_request(func: Callable[..., Any], **kwargs: dict[str, Any]) -> tuple[str, Request]:
    for key, value in kwargs.items():
        if isinstance(value, Request):
            return key, value

    raise AttributeError(f'Request object not found in {func.__module__}.{func.__name__}')


def idempotent(
        expire: int = settings.CACHE_CONFIG.IDEMPOTENTY_TIMER,
        namespace: str = '',
):
    """
    Делает идемпотентрыми POST/PATCH запросы на определенное время.
    Требуется в заголовке передавать уникальный Idempotency-Key.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> JSONResponse | BaseModel:
            key_request, request = find_request(func, **kwargs)

            idempotency_key = request.headers.get('Idempotency-Key')
            if not idempotency_key:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=IDEMPOTENCY_KEY_NOT_FOUND,
                )

            if settings.REDIS_DSN is None:
                return await func(*args, **kwargs)

            copy_kwargs = kwargs.copy()
            copy_kwargs.pop(key_request)
            redis_client: Redis = request.app.state.main_app.redis_client
            cache_key = key_builder(func, namespace, idempotency_key=idempotency_key, args=args, kwargs=copy_kwargs)

            cached_response = await redis_client.get(cache_key)
            if cached_response:
                response_data = json.loads(cached_response)
                return JSONResponse(
                    content=response_data,
                    headers={
                        'X-Response-Source': 'idempotency-cache',
                        'X-Cache-Expires-In': str(await redis_client.ttl(cache_key)),
                    },
                )

            result: BaseModel = await func(*args, **kwargs)
            response_data = result.model_dump_json()
            await redis_client.setex(
                cache_key,
                expire,
                response_data,
            )

            return result

        return wrapper
    return decorator
