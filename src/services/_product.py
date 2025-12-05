import datetime
from collections.abc import AsyncGenerator, Sequence

from fastapi import Depends
from sqlalchemy import desc, func, select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from env_settings import settings
from orm import get_async_session
from orm.models import Product, ProductType, Transaction, TransactionStatus

from ._base import DatabaseService


class ProductDatabaseService(DatabaseService):
    model = Product

    async def get_by_id(self, product_id: int) -> Product | None:
        statement = select(self.model).where(self.model.id == product_id)
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def add_product(
            self,
            name: str,
            price: int,
            product_type: ProductType,
            description: str | None = None,
    ) -> Product:
        product = self.model(
            name=name,
            price=price,
            type=product_type.value,
            description=description,
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_popular_products(self) -> Sequence[Row[tuple[Product, int]]]:
        timedelta = (
            datetime.datetime.now().astimezone() -
            datetime.timedelta(days=settings.API_SETTINGS.LAST_DAYS_NUMBER)
        )
        statement = (
            select(self.model, func.count(Transaction.id).label('purchase_count'))
            .join(Transaction, Transaction.product_id == self.model.id)
            .where(
                Transaction.created_at >= timedelta,
                Transaction.status == TransactionStatus.completed,
            )
            .group_by(self.model.id)
            .order_by(desc('purchase_count'))
            .limit(5)
        )

        result = await self.session.execute(statement)
        return result.all()


async def get_product_database_service(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[ProductDatabaseService]:
    yield ProductDatabaseService(session)
