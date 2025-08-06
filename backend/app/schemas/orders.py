from pydantic import BaseModel
from typing import List

class OrderCreateBase(BaseModel):
    item_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderCreateBase]

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    items: list[OrderCreateBase]

    model_config = {
        "from attributes": True
    }