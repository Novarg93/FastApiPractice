from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    image = Column(String(100), nullable=True)
    description = Column(String, nullable=True)

    categories = relationship("Category", back_populates="game")
    items = relationship("Item", back_populates="game")
