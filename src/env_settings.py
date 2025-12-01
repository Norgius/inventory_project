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
    """Таймер идемпотентности в секундах для POST/PUTCH запросов,
    при условии, что на них навешан декоратор idempotent
    """
    NAMESPACE: CacheNamespace = CacheNamespace()


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

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        validate_default=True,
        extra='forbid',
        use_attribute_docstrings=True,
    )


settings = ENV()
