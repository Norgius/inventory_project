import datetime
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import get_async_session
from orm.models import Inventory, Product, ProductType

from ._base import DatabaseService
from ._user import User
from .exceptions import InventoryNotFoundError, NotEnoughProductInInventoryError, PermanentProductUsingError


class InventoryDatabaseService(DatabaseService):
    model = Inventory

    async def get_or_create(
            self,
            user_id: int,
            product: Product,
    ) -> tuple[Inventory, bool]:
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.product_id == product.id))
        result = await self.session.execute(statement=statement)
        inventory = result.unique().scalar_one_or_none()
        created = False
        if inventory is None:
            inventory = self.model(
                user_id=user_id,
                product_id=product.id,
                quantity=1 if product.type == ProductType.consumable else None,
                purchased_at=datetime.datetime.now().astimezone(),
            )
            created = True
        self.session.add(inventory)
        return inventory, created

    async def increase_product_quantity(self, inventory: Inventory) -> None:
        inventory.quantity += 1
        inventory.purchased_at = datetime.datetime.now().astimezone()
        self.session.add(inventory)

    async def get_user_inventories(self, user_id: int) -> list[Inventory]:
        statement = (
            select(self.model)
            .options(joinedload(self.model.product))
            .join(User, self.model.user_id == User.id)
            .where(self.model.user_id == user_id)
            .order_by(-self.model.quantity)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def use_product(self, product_id: int, user_id: int) -> Inventory | None:
        statement = (
            select(self.model)
            .options(joinedload(self.model.product))
            .where(self.model.product_id == product_id, self.model.user_id == user_id)
        )
        result = await self.session.execute(statement)
        inventory = result.scalar_one_or_none()
        if inventory is None:
            raise InventoryNotFoundError
        if inventory.product.type == ProductType.permanent:
            raise PermanentProductUsingError
        if inventory.quantity == 0:
            raise NotEnoughProductInInventoryError
        inventory.quantity -= 1
        self.session.add(inventory)
        await self.session.commit()
        await self.session.refresh(inventory)
        return inventory


async def get_inventory_database_service(
        session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[InventoryDatabaseService]:
    yield InventoryDatabaseService(session)
