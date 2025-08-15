from pydantic import BaseModel
from typing import List, Optional
from app.schemas.users import UserRead
from app.schemas.items import ItemRead

class OrderItemRead(BaseModel):
    id: int
    item_id: int
    quantity: int
    price: float
    item: Optional[ItemRead] = None

    model_config = {"from_attributes": True}

class OrderCreateItem(BaseModel):
    item_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderCreateItem]

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    items: List[OrderItemRead]
    user: Optional[UserRead] = None

    model_config = {"from_attributes": True}
