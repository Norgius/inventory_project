import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .._db import Base

USERNAME_MAX_LENGTH = 254


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        String(USERNAME_MAX_LENGTH),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        nullable=True,
    )
    balance: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    inventories = relationship('Inventory', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now().astimezone(),
        nullable=False,
    )

    def __str__(self) -> str:
        return self.username
