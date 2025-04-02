from typing import Optional
import uuid
from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint
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

    __table_args__ = (
        UniqueConstraint("email", "provider", name="unique_email_per_provider"),
    )

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
