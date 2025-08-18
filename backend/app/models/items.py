from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String)
    quantity = Column(Integer)
    quality = Column(Integer)

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)

    game = relationship("Game", back_populates="items")
    category = relationship("Category", back_populates="items")
    order_items = relationship('OrderItem', back_populates='item')
