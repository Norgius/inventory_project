import pytest
from fastapi_cache import FastAPICache
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from env_settings import settings

from .mock_data.mock_inventories import mock_inventories
from .mock_data.mock_products import mock_products
from .mock_data.mock_transactions import mock_transactions
from .mock_data.mock_users import mock_users


@pytest.fixture(scope="session", autouse=True)
async def prepere_database():
    assert 'db_test' in settings.POSTGRES_DSN.path  # type: ignore

    from orm import Base, async_session_maker, engine
    from orm.models import Inventory, Product, Transaction, User

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        users = insert(User).values(mock_users)
        products = insert(Product).values(mock_products)
        inventories = insert(Inventory).values(mock_inventories)
        transactions = insert(Transaction).values(mock_transactions)

        await session.execute(users)
        await session.execute(products)
        await session.execute(inventories)
        await session.execute(transactions)

        await session.commit()


@pytest.fixture(scope='function')
async def client():
    from main import app as fastapi_app

    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope='function')
async def session():
    from orm import async_session_maker

    async with async_session_maker() as session:
        try:
            transaction = await session.begin()
            yield session
        finally:
            await transaction.rollback()


@pytest.fixture(scope='function')
async def clear_cache():
    all_cache_namespaces = settings.CACHE_CONFIG.NAMESPACE.model_dump().values()
    for namespace in all_cache_namespaces:
        await FastAPICache.clear(namespace)
