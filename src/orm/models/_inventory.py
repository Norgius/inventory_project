import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ._product import ProductType
from .._db import Base

if TYPE_CHECKING:
    from ._product import Product
    from ._user import User


class Inventory(Base):
    __tablename__ = 'inventories'

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_positive_quantity"),
        UniqueConstraint("user_id", "product_id", name="unique_user_product"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    user: Mapped['User'] = relationship(
        back_populates='inventories',
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='RESTRICT'),
        nullable=False,
    )
    product: Mapped['Product'] = relationship()
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    purchased_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    @validates('quantity')
    def validate_quantity(self, key: Any, quantity: int | None) -> int:
        if self.product and self.product.type == ProductType.permanent and quantity is not None:
            raise ValueError("Permanent products can not have quantity")
        if self.product and self.product.type == ProductType.consumable and quantity is None:
            raise ValueError("Consumable products must have quantity")
        return quantity

    def __str__(self):
        return f'inventory {self.id}'
