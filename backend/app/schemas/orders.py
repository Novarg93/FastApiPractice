from datetime import datetime

from pydantic import BaseModel, conint, confloat, field_validator
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
    quantity: conint(gt=0)
    price: confloat(gt=0)

class OrderCreate(BaseModel):
    items: List[OrderCreateItem]

    @field_validator("items")
    def check_items(cls, v):
        if not v:
            raise ValueError("Items must contain at least 1 item")
        return v

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    created_at: datetime
    updated_at: datetime | None = None
    items: List[OrderItemRead]
    user: Optional[UserRead] = None

    model_config = {"from_attributes": True}
