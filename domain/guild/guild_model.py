import uuid
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped
from infrastructure.database.database import Base
from domain.user.user_model import User

class Guild(Base):
    __tablename__ = "guild"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey(User.id), nullable=False)
    name = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    disable = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
     
    user : Mapped["User"] = relationship("User", back_populates="guild")
     
    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
