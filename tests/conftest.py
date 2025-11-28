import asyncio

import pytest
from sqlalchemy import insert

from env_settings import settings
from orm import Base, async_session_maker, engine
from orm.models import Product, User, Transaction, Inventory
from .mock_data.mock_inventories import mock_inventories
from .mock_data.mock_products import mock_products
from .mock_data.mock_users import mock_users
from .mock_data.mock_transactions import mock_transactions


@pytest.fixture(scope="session", autouse=True)
async def prepere_database():
    assert 'db_test' in settings.POSTGRES_DSN.path

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


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
