from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, Index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.now)
    user = relationship('User', backref='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, Index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    item_id = Column(Integer, ForeignKey('items_id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)

    order = relationship('Order', backref='items')
    item = relationship('Item')
