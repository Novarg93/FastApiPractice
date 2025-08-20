from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.session import Base


class ItemOption(Base):
    __tablename__ = "item_options"   # множественное, как принято

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    key = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    label = Column(String, nullable=False)

    item = relationship("Item", back_populates="options")
    choices = relationship("ItemOptionChoice", back_populates="option", cascade="all, delete-orphan")


class ItemOptionChoice(Base):
    __tablename__ = "item_option_choices"

    id = Column(Integer, primary_key=True, index=True)
    option_id = Column(Integer, ForeignKey("item_options.id", ondelete="CASCADE"), nullable=False)
    value = Column(String, nullable=False)
    label = Column(String, nullable=False)
    pct = Column(Float, nullable=True)
    abs_cents = Column(Float, nullable=True)
    multiplier = Column(Float, nullable=True)
    order = Column(Integer, nullable=True)

    option = relationship("ItemOption", back_populates="choices")
