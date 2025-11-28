from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, drop_database, create_database

from env_settings import ENV

envs = ENV()


class Base(DeclarativeBase):
    pass


postgres_dsn = envs.POSTGRES_DSN

engine = create_async_engine(str(postgres_dsn))

# if 'test' in str(postgres_dsn):
#     if not database_exists(engine.url):
#         drop_database(engine.url)

#     create_database(engine.url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
