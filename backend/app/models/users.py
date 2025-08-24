from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserRole(str, Enum):
    USER = 'user'
    BOOSTER = 'booster'
    SUPPORT = 'support'
    ADMIN = 'admin'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String(512), nullable=True)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete")
    messages = relationship("Message", back_populates="sender", cascade="all, delete")
    chat_participations = relationship("ChatParticipant", back_populates="user", cascade="all, delete")
