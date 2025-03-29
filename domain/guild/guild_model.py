import uuid
from typing import List
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from infrastructure.database.database import Base

class Guild(Base):
    __tablename__ = "guild"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    disable = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    
    # Relation One-to-One : un propriétaire de guilde
    owner = relationship("User", back_populates="owned_guild", foreign_keys="[User.owned_guild_id]", uselist=False)

    # Relation One-to-Many : une guilde a plusieurs membres
    members = relationship("User", back_populates="guild", foreign_keys="[User.guild_id]")

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
