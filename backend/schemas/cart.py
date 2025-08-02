from pydantic import BaseModel
from typing import List
from schemas.items import ItemRead

class CartItemRead(BaseModel):
    item: ItemRead
    quantity: int

    class Config:
        from_attributes = True

class CartRead(BaseModel):
    items: List[CartItemRead]
    total_price: float
    count: int

    class Config:
        from_attributes = True

class CartAdd(BaseModel):
    item_id: int
    quantity: int

class CartRemove(BaseModel):
    item_id: int
