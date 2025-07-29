from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)        # хранится в копейках
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)

    # Связь с позициями заказов
    order_items = relationship("OrderItem", back_populates="item")
