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
    guild_members: Mapped[List["User"]] = relationship("User", foreign_keys="[User.my_guild_id]")
    owner: Mapped["User"] = relationship("User", back_populates="ownered_guild", foreign_keys="[User.ownered_guild_id]")

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
