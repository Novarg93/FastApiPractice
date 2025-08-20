from platform import release

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base

class ItemOption(Base):
    __tablename__ = "item_option"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item.id", ondelete="CASCADE"))
    key = Column(String,nullable=False, index=True)
    type = Column(String, nullable=False)
    label = Column(String, nullable=False)

    choices = relationship("ItemOptionChoice", back_populates="option", cascade="all, delete-orphan")
    item = relationship("Item", back_populates="options")

class ItemOptionChoice(Base):
    __tablename__ = "item_option_choice"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item.option.id", ondelete="CASCADE"))
    value = Column(String, nullable=False)
    label = Column(String, nullable=False)
    pct = Column(Float, nullable=True)
    abs_cents = Column(Float, nullable=True)
    multiplier = Column(Float, nullable=True)
    order = Column(Integer, nullable=True)

    option = relationship("ItemOption", back_populates="choices")
