from typing import Any, Type
from unittest.mock import Base

from infrastructure.database.transaction import transaction
from sqlalchemy import delete, select, and_, update
from sqlalchemy.engine import Result

from infrastructure.error.error import NotFoundError



class BaseRepository:
    schema: Type[Base]
    
    
    async def _get(self, **kwargs) -> Base:
        """Return only one result by filters"""
        conditions = [getattr(self.schema_class, key) == value for key, value in kwargs.items()]
        query = select(self.schema_class).where(and_(*conditions))
        
        async with transaction() as session:
            result: Result = await session.execute(query)
            _result = result.scalars().one_or_none()
            
            
            if _result is None:
                raise NotFoundError(ressource=self.schema_class.__name__ + " with this conditions: " + " and ".join(list(kwargs.keys())))

            return _result.__dict__


    async def _save(self, instance: Base) -> Base:
        """Save or update an instance"""
        async with transaction() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance.__dict__
        
    async def _delete(self, **kwargs) -> None:
        conditions = [getattr(self.schema_class, key) == value for key, value in kwargs.items()]
        query = delete(self.schema_class).where(and_(*conditions))
        
        async with transaction() as session:
            await session.execute(query)
            await session.commit()
            
    async def _update(self, instance: Base) -> Base:
        async with transaction() as session:
            merged_instance = await session.merge(instance)
            await session.commit()
            await session.refresh(merged_instance)
            return merged_instance.__dict__
    