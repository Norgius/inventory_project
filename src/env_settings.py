from typing import Literal

from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RateLimiterSettings(BaseModel):
    TIMES: int = 10
    SECONDS: int = 10


class CacheNamespace(BaseModel):
    ADD_FUNDS: str = 'add-funds'
    POPULAR_PRODUCTS: str = 'popular-products'


class CacheConfig(BaseModel):
    PREFIX: str = 'fastapi-cache'
    IDEMPOTENTY_TIMER: int = 3600
    """Время идемпотентности для POST/PUTCH запросов в секундах,
    параметр необходим для декоратора idempotent
    """
    POPULAR_PRODUCT_TIMER: int = 900
    """Время кеширования для эндпоинта популярных продуктов в секундах."""
    NAMESPACE: CacheNamespace = CacheNamespace()


class ApiSettings(BaseModel):
    LAST_DAYS_NUMBER: int = 7
    """Кол-во последних дней для endpoints аналитики."""


class ENV(BaseSettings):
    MODE: Literal['dev', 'test', 'prod']
    POSTGRES_DSN: PostgresDsn
    """Подключение к PostgreSQL."""
    REDIS_DSN: RedisDsn | None = None
    """Подключение к Redis."""
    CACHE_CONFIG: CacheConfig = CacheConfig()
    """Настройки для кэша"""
    RATE_LIMITER: RateLimiterSettings = RateLimiterSettings()
    """Настройки для ограничения кол-ва запросов за отведенное время."""
    API_SETTINGS: ApiSettings = ApiSettings()
    """Настройки для параметров api endpoints."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        validate_default=True,
        extra='forbid',
        use_attribute_docstrings=True,
    )


settings = ENV()
