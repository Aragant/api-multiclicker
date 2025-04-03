from typing import Type
from unittest.mock import Base

from infrastructure.database.transaction import transaction
from sqlalchemy import delete, select, and_
from sqlalchemy.engine import Result


class BaseRepository:
    def __init__(self, schema: Type[Base], transaction=transaction):
        self.schema_class = schema
        self.transaction = transaction

    async def _get(self, options: list = None, **kwargs) -> Base:
        """Return only one result by filters"""
        conditions = [
            getattr(self.schema_class, key) == value for key, value in kwargs.items()
        ]
        query = select(self.schema_class).where(and_(*conditions))

        if options:
            query = query.options(*options)
            
        async with self.transaction() as session:
            result: Result = await session.execute(query)
            _result = result.scalars().one_or_none()

            if _result is None:
                return None

            return _result.__dict__

    async def _get_all(self, options: list = None) -> Base:
        """Return all results with optional relation loading"""
        query = select(self.schema_class)

        if options:
            query = query.options(*options)

        async with self.transaction() as session:
            result: Result = await session.execute(query)
            return result.scalars().all()

    async def _save(self, instance: Base) -> Base:
        """Save or update an instance"""
        async with self.transaction() as session:
            session.add(instance)
            await session.flush()
            await session.refresh(instance)
            return instance.__dict__

    async def _delete(self, **kwargs) -> None:
        conditions = [
            getattr(self.schema_class, key) == value for key, value in kwargs.items()
        ]
        query = delete(self.schema_class).where(and_(*conditions))

        async with self.transaction() as session:
            await session.execute(query)
            await session.flush()

    async def _update(self, instance: Base) -> Base:
        async with self.transaction() as session:
            merged_instance = await session.merge(instance)
            await session.flush()
            await session.refresh(merged_instance)
            return merged_instance.__dict__
