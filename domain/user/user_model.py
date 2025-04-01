from typing import Optional
import uuid
from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from infrastructure.database.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    username = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)
    provider = Column(String, default="local", nullable=True)
    email = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    register_date = Column(DateTime, default=func.now())
    
    # Relation Many-to-Many via Member
    members = relationship("Member", back_populates="user", cascade="all, delete-orphan")

<<<<<<< HEAD
=======
    # Relation One-to-One : un utilisateur peut posséder une seule guilde
    owned_guild_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("guild.id", ondelete="SET NULL"), unique=True
    )
    owned_guild = relationship(
        "Guild", back_populates="owner", foreign_keys=[owned_guild_id], uselist=False
    )

    # Relation Many-to-One : un utilisateur peut appartenir à une guilde
    guild_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("guild.id", ondelete="SET NULL")
    )
    guild = relationship("Guild", back_populates="members", foreign_keys=[guild_id])

>>>>>>> 79ad7e7e66648ea30a86996706fbace9a4e9ab49
    __table_args__ = (
        UniqueConstraint("email", "provider", name="unique_email_per_provider"),
    )

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
