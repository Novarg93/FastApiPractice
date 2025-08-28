from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# 🔹 Значение опции (Choice)
class OptionChoiceSchema(BaseModel):
    id: int
    value: str
    label: str
    pct: Optional[float] = None
    abs_cents: Optional[int] = None
    multiplier: Optional[float] = None
    sort_order: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class OptionChoiceCreate(BaseModel):
    value: str
    label: str
    pct: Optional[float] = None
    abs_cents: Optional[int] = None
    multiplier: Optional[float] = None
    sort_order: Optional[int] = None


class OptionChoiceUpdate(BaseModel):
    value: Optional[str] = None
    label: Optional[str] = None
    pct: Optional[float] = None
    abs_cents: Optional[int] = None
    multiplier: Optional[float] = None
    sort_order: Optional[int] = None


# 🔹 Опция
class OptionSchema(BaseModel):
    id: int
    name: str
    type: str
    label: str
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None

    choices: List[OptionChoiceSchema] = []

    model_config = ConfigDict(from_attributes=True)


class OptionCreate(BaseModel):
    name: str
    type: str
    label: str
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None


class OptionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    label: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None


# 🔹 Связь товара и опции
class ProductOptionCreate(BaseModel):
    is_required: bool = False
    sort_order: int = 0


class ProductOptionRead(ProductOptionCreate):
    product_id: int
    option_id: int

    model_config = ConfigDict(from_attributes=True)
