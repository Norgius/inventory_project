import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .._db import Base

if TYPE_CHECKING:
    from orm.models import Product, User


class TransactionStatus(enum.Enum):
    pending = 'pending'
    completed = 'completed'
    failed = 'failed'


class Transaction(Base):
    __tablename__ = 'transactions'

    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_positive_amount"),
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
        back_populates='transactions',
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='RESTRICT'),
        nullable=False,
    )
    product: Mapped['Product'] = relationship()
    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus),
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now().astimezone(),
        nullable=False,
    )

    def __str__(self) -> str:
        return f'{self.id} from {self.created_at}'
