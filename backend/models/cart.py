from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart")
    item = relationship("Item", back_populates="cart_items")
