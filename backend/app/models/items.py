from sqlalchemy import Column, Integer, String, Float
from app.database.session import Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    quality = Column(Integer, nullable=True)