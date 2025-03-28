import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class Guild(Base):
    __tablename__ = "guild"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    disable = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
