from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")