from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from domain.user.user_model import User
from infrastructure.database.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(User.id), nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(days=7))
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)