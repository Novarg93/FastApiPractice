from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String)
    quantity = Column(Integer)
    quality = Column(String)

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)
    order_items = relationship('OrderItem', back_populates='item')

    game = relationship("Game", back_populates="items")
    categories = relationship(
        "Category",
        secondary="item_categories",
        back_populates="items"
    )

