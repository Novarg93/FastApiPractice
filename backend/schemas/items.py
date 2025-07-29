from pydantic import BaseModel, HttpUrl
from typing import Optional

class ItemBase(BaseModel):
    title: str
    price: float
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    class Config:
        orm_mode = True

class Category(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class Inventory(BaseModel):
    item_id: int
    quantity: int

class Review(BaseModel):
    user_id: int
    item_id: int
    rating: int
    comment: Optional[str] = None
