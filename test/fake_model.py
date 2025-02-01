from sqlalchemy import Column, Integer, String
from infrastructure.database.database import Base

class FakeModel(Base):
    __tablename__ = "fake_model"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=False)