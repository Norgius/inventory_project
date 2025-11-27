import enum

from sqlalchemy import Boolean, CheckConstraint, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .._db import Base


class ProductType(enum.Enum):
    consumable = "consumable"
    permanent = "permanent"


class Product(Base):
    __tablename__ = 'products'

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_positive_price"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    type: Mapped[ProductType] = mapped_column(
        Enum(ProductType),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    def __str__(self) -> str:
        return self.name
