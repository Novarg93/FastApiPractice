from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from database.session import Base
import enum

class ItemType(enum.Enum):
    quantitative = "quantitative"
    qualitative = "qualitative"

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    type = Column(Enum(ItemType), nullable=False)
    quantity = Column(Integer)      # для количественных товаров
    quality = Column(String)        # для качественных товаров (например, "1-20 lvl")
    favorites = relationship("Favorite", back_populates="item")
    cart_items = relationship("Cart", back_populates="item")
