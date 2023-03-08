from typing import Any, Generic, List, TypeVar

from sqlalchemy import inspect, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")


class CRUDMixin(Generic[T]):
    """Mixin for CRUD operations for models."""

    @classmethod
    async def create(cls, session: AsyncSession, model_data: Any) -> T:
        """Get object by pk column."""
        query = insert(cls).values(**model_data)
        res = await session.execute(query)
        return res.inserted_primary_key[0]  # type: ignore # pr

    @classmethod
    async def get(cls, session: AsyncSession, pk_val: Any) -> T:
        """Get object by pk column."""
        pkey_column = inspect(cls).primary_key[0]
        query = select(cls).where(pkey_column == pk_val)
        rows = await session.execute(query)
        return rows.scalars().one()

    @classmethod
    async def all(cls, session: AsyncSession) -> List[T]:
        """Get all objects."""
        query = select(cls)
        rows = await session.execute(query)
        return rows.scalars().all()

    @classmethod
    async def update(
        cls,
        *,
        session: AsyncSession,
        pkey_val: Any,
        model_data: dict[str, Any],
    ) -> None:
        """Update object by primary key."""
        pkey_column = inspect(cls).primary_key[0]
        query = (
            update(cls)
            .where(pkey_column == pkey_val)
            .values(**model_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
