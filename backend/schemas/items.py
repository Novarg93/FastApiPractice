from pydantic import BaseModel, Field
from typing import Optional
import enum

class ItemType(str, enum.Enum):
    quantitative = "quantitative"
    qualitative = "qualitative"

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    type: ItemType
    quantity: Optional[int] = None     # только для количественных
    quality: Optional[str] = None      # только для качественных

    class Config:
        from_attributes = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    image_url: Optional[str]
    type: Optional[ItemType]
    quantity: Optional[int]
    quality: Optional[str]

    class Config:
        from_attributes = True

class ItemRead(ItemBase):
    id: int
    is_favorite: Optional[bool] = False  # вычисляемое поле для каталога

    class Config:
        from_attributes = True
