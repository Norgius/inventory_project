

import hashlib
from typing import Any, Callable

from fastapi import Request, Response

from services import DatabaseService


def check_balance(user_balance: int, product_price: int) -> tuple[int, bool]:
    difference = user_balance - product_price
    low_balance = False
    if difference < 0:
        difference = abs(difference)
        low_balance = True
    return difference, low_balance


def key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Request | None = None,
    response: Response | None = None,
    idempotency_key: str = '',
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    """Генерация уникального ключа."""
    exclude_types = (DatabaseService,)
    cache_kwargs = {}
    for key, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        cache_kwargs[key] = value

    cache_key = hashlib.md5(
        f'{func.__module__}:{func.__name__}:{args}:{cache_kwargs}:{idempotency_key}'.encode()
    ).hexdigest()
    return f'{namespace}:{cache_key}'