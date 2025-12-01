from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseService:  # noqa: B903
    def __init__(self, session: AsyncSession):
        self.session = session
