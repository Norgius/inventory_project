from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from orm import get_async_session
from orm.models import Product, ProductType, Transaction, TransactionStatus, User

from ._base import DatabaseService
from ._inventory import InventoryDatabaseService


class TransactionDatabaseService(DatabaseService):
    model = Transaction

    async def purchase_product(self, user: User, product: Product):
        user.balance -= product.price
        self.session.add(user)

        inventory_database_service = InventoryDatabaseService(session=self.session)
        inventory, created = await inventory_database_service.get_or_create(
            user_id=user.id,
            product=product,
        )
        if not created and product.type == ProductType.consumable:
            await inventory_database_service.increase_product_quantity(inventory=inventory)

        transaction = self.model(
            user_id=user.id,
            product_id=product.id,
            amount=product.price,
            status=TransactionStatus.completed,
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(inventory)
        return inventory


async def get_transaction_database_service(
        session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[TransactionDatabaseService]:
    yield TransactionDatabaseService(session)
