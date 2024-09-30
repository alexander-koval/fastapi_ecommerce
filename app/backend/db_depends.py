from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db import async_session_maker


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


class SessionContextManager:

    def __init__(self) -> None:
        self.session_factory = async_session_maker
        self.session = None

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(self, *args: object) -> None:
        await self.rollback()

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()
            await self.session.close()
        self.session = None

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
            await self.session.close()
        self.session = None
