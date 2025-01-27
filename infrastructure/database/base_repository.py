from typing import Any, Generic, Type

from pydantic import ValidationError
from infrastructure.database.transaction import transaction
from infrastructure.database.database import ConcreteTable
from sqlalchemy import select
from sqlalchemy.engine import Result

from infrastructure.error.error import NotFoundError
from user.user_schema import UserFlat


class BaseRepository:
    schema: Type[ConcreteTable]
    
    
    async def _get(self, key: str, value: Any) -> ConcreteTable:
        """Return only one result by filters"""
        
        query = select(self.schema_class).where(
            getattr(self.schema_class, key) == value
        )
        
        async with transaction() as session:
            result: Result = await session.execute(query)
            _result = result.scalars().one_or_none()
            
            
            if _result is None:
                raise NotFoundError(ressource=value) 

            return _result.__dict__
        
    async def _save(self, instance: ConcreteTable) -> ConcreteTable:
        """Save or update an instance"""
        async with transaction() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance.__dict__
    