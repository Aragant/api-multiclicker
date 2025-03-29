import uuid
import dataclasses
from enum import Enum
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from infrastructure.database.database import Base

class MemberRight(Enum):
    PENDING = 0
    MEMBER = 1
    MASTER = 2
    
@dataclasses.dataclass
class Member(Base):
    """Member Model"""

    __tablename__ = "member"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    guild_id: Mapped[str] = mapped_column(ForeignKey("guild.id", ondelete="SET NULL"), nullable=False)
    right = Column(Integer, default=MemberRight.PENDING.value)

    # Relation One-to-Many : un membre appartient à une guilde
    guild = relationship("Guild", back_populates="members")

    # Relation One-to-Many : un membre appartient à un utilisateur
    user = relationship("User", back_populates="members")
    
    @property
    def as_dict(self):
        """Returns the object as a dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}