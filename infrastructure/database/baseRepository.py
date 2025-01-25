from typing import Generic, Type
from infrastructure.database.database import ConcreteTable
from sqlalchemy import select
from sqlalchemy.engine import Result


class BaseRepository:
    schema: Type[ConcreteTable]
    
    
    async def _get(self, key: str, value: Any) -> ConcreteTable:
        """Return only one result by filters"""
        
        query = select(self.schema_class).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)
        _result = result.scalars().one_or_none()
        
        if _result is None:
            raise NotFoundError 

        return _result