from sqlalchemy import Column, Integer, String
from app.database.session import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    short_description = Column(String, nullable=True)
    description = Column(String, nullable=True)
    seo_description = Column(String, nullable=False)

