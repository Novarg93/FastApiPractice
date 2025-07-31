from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    favorites = relationship("Favorite", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    user = relationship("User", back_populates="favorites")
    item = relationship("Item", back_populates="favorites")
    __table_args__ = (UniqueConstraint('user_id', 'item_id', name='unique_favorite'),)
