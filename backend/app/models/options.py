from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)   # method, speed, quantity
    type = Column(String(20), nullable=False)                # radio, slider, select
    label = Column(String(100), nullable=False)
    min_value = Column(Integer, nullable=True)
    max_value = Column(Integer, nullable=True)
    step = Column(Integer, nullable=True)

    # связи
    choices = relationship(
        "OptionChoice",
        back_populates="option",
        cascade="all, delete-orphan"
    )

    product_options = relationship(
        "ProductOption",
        back_populates="option",
        cascade="all, delete-orphan"
    )

    # виртуальная связь (только для чтения)
    items = relationship("Item", secondary="product_options", viewonly=True)


class OptionChoice(Base):
    __tablename__ = "option_choices"

    id = Column(Integer, primary_key=True, index=True)
    option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    value = Column(String(50), nullable=False)
    label = Column(String(100), nullable=False)
    pct = Column(Float, default=0)          # процентная надбавка
    abs_cents = Column(Integer, default=0)  # фиксированная надбавка
    multiplier = Column(Float, default=1.0)
    sort_order = Column(Integer, default=0)

    option = relationship("Option", back_populates="choices")


class ProductOption(Base):
    __tablename__ = "product_options"

    product_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"), primary_key=True)

    # дополнительные поля
    is_required = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    # связи
    item = relationship("Item", back_populates="product_options")
    option = relationship("Option", back_populates="product_options")
