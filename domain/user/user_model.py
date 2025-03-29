import uuid
from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from infrastructure.database.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    provider = Column(String, default="local", nullable=True)
    email = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    register_date = Column(DateTime, default=func.now())
    my_guild_id: Mapped[str] = mapped_column(ForeignKey("guild.id"), nullable=True)
    ownered_guild_id: Mapped[str] = mapped_column(ForeignKey("guild.id"), nullable=True)
    __table_args__ = (UniqueConstraint('email', 'provider', name='unique_email_per_provider'),)

    ownered_guild: Mapped["Guild"] = relationship("Guild", back_populates="owner", foreign_keys=[ownered_guild_id])
    my_guild: Mapped["Guild"] = relationship("Guild", foreign_keys=[my_guild_id])

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
