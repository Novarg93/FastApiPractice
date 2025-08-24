from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.session import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)

    game = relationship("Game", back_populates="categories")
    items = relationship(
        "Item",
        secondary="item_categories",
        back_populates="categories"
    )

    item_categories = Table(
        "item_categories",
        Base.metadata,
        Column("item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
        Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    )