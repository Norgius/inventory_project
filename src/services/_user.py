from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from orm import get_async_session
from orm.models import User

from ._base import DatabaseService
from .exceptions import UserAlreadyExistsError


class UserDatabaseService(DatabaseService):
    model = User

    async def create(self, username: str, email: str) -> User:
        user = self.model(username=username, email=email)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise UserAlreadyExistsError
            raise
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id) -> User | None:
        statement = select(self.model).where(self.model.id == user_id)
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def add_funds(self, user: User, amount: int) -> User:
        user.balance += amount
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


async def get_user_database_service(
        session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[UserDatabaseService]:
    yield UserDatabaseService(session)
