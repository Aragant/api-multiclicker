from typing import Any, Type

from infrastructure.database.transaction import transaction
from infrastructure.database.database import ConcreteTable
from sqlalchemy import select, and_
from sqlalchemy.engine import Result

from infrastructure.error.error import NotFoundError



class BaseRepository:
    schema: Type[ConcreteTable]
    
    
    async def _get(self, **kwargs) -> ConcreteTable:
        """Return only one result by filters"""
        conditions = [getattr(self.schema_class, key) == value for key, value in kwargs.items()]
        query = select(self.schema_class).where(and_(*conditions))
        
        async with transaction() as session:
            result: Result = await session.execute(query)
            _result = result.scalars().one_or_none()
            
            
            if _result is None:
                raise NotFoundError(ressource=self.schema_class.__name__ + " with this conditions: " + " and ".join(list(kwargs.keys())))

            return _result.__dict__


    async def _save(self, instance: ConcreteTable) -> ConcreteTable:
        """Save or update an instance"""
        async with transaction() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance.__dict__
    