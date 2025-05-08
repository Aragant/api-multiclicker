from typing import Optional, Type
from unittest.mock import Base

from infrastructure.database.transaction import transaction
from sqlalchemy import delete, select, and_
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload, Load


class BaseRepository:
    def __init__(self, schema: Type[Base], transaction=transaction):
        self.schema_class = schema
        self.transaction = transaction

    async def _get(self, options: list = None, **kwargs) -> Base:
        """Return only one result by filters"""
        conditions = []
        for key, value in kwargs.items():
            column = getattr(self.schema_class, key)
            if isinstance(value, list):
                conditions.append(column.in_(value))
            else:
                conditions.append(column == value)

        query = select(self.schema_class).where(and_(*conditions))

        if options:
            query = query.options(*options)

        async with self.transaction() as session:
            result: Result = await session.execute(query)
            _result = result.scalars().one_or_none()

            if _result is None:
                return None

            return _result.__dict__

    # async def _get_all_with_option(self, options: Optional[list] = None) -> list[dict]:
    #     """Return all results with optional relation loading based on relationship chain"""
    #     query = select(self.schema_class)

    #     if options:
    #         # On construit dynamiquement les selectinload imbriqués
    #         loader = selectinload(options[0])
    #         for relation in options[1:]:
    #             loader = loader.selectinload(relation)
    #         query = query.options(loader)

    #     async with self.transaction() as session:
    #         result: Result = await session.execute(query)
    #         instances = result.scalars().all()
    #         return [instance.__dict__ for instance in instances]

    async def _get_multiple(self, options: list = None, **kwargs) -> list[dict]:
        """Return multiple results by filters"""
        conditions = []
        for key, value in kwargs.items():
            column = getattr(self.schema_class, key)
            if isinstance(value, list):
                conditions.append(column.in_(value))
            else:
                conditions.append(column == value)

        query = select(self.schema_class).where(and_(*conditions))

        if options:
            query = query.options(*options)

        async with self.transaction() as session:
            result: Result = await session.execute(query)
            instances = result.scalars().all()
            return [instance.__dict__ for instance in instances]


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


    async def _execute_query(self, query) -> Base:
        async with self.transaction() as session:
            result = await session.execute(query)
            instances = result.scalars().all()
            
            return instances